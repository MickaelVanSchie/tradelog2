from flask import redirect, request, flash, Response
import os

from blueprints.app import main_app
from blueprints.exceptions.position_store import PositionStoreException
from config.database import db
from models import Position
from models.position_image import PositionImage
import uuid
from sqlalchemy import select

UPLOAD_FOLDER = 'uploads/position_images'


def store_position(entry: float, take_profit: float, stop_loss: float, pair: uuid.UUID, reason: str,
                   size: float) -> Position | None:
    try:
        position = Position(
            id=uuid.uuid4(),
            type="long" if take_profit > entry else "short",
            entry=entry,
            take_profit=float(take_profit),
            stop_loss=float(stop_loss),
            position_size=float(size),
            pair_id=pair,
            opening_reason=reason,
        )

        db.add(position)
        db.commit()
        return position
    except PositionStoreException:
        db.rollback()
        return None


@main_app.post('/create-position')
def create_position() -> Response:
    try:
        entry = float(request.form.get('entry'))
        take_profit = float(request.form.get('take_profit'))
        stop_loss = float(request.form.get('stop_loss'))
        pair = uuid.UUID(request.form.get('pair'))
        reason = request.form.get('reason')
        size = float(request.form.get('size'))

        store_position(entry, take_profit, stop_loss, pair, reason, size)

        return redirect('/')
    except (ValueError, TypeError):
        flash("Invalid input. Please ensure all fields are filled correctly.", "danger")
        return redirect(request.referrer)
    except PositionStoreException:
        flash("An error occurred while storing your position. Please try again later.", "danger")
        return redirect(request.referrer)


@main_app.post('upload-position-image')
def upload_position_image() -> Response:
    try:
        if 'image' not in request.files:
            flash("No image file provided.", "danger")
            return redirect(request.referrer)

        file = request.files['image']
        if file.filename == '':
            flash("No image selected.", "danger")
            return redirect(request.referrer)

        position_id = request.form.get('position_id')
        img_name = file.filename
        extension = img_name.split('.')[-1]
        image_uuid = uuid.uuid4()

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        image_type = request.form.get('type', "open")
        existing_image = db.execute(
            select(PositionImage).where(
                PositionImage.position_id == uuid.UUID(position_id),
                PositionImage.type == image_type
            )
        ).scalar_one_or_none()

        if existing_image:
            old_filepath = os.path.join(UPLOAD_FOLDER, f"{existing_image.id}.{existing_image.extension}")
            if os.path.exists(old_filepath):
                os.remove(old_filepath)

            existing_image.id = image_uuid
            existing_image.extension = extension
        else:
            position_image = PositionImage(
                id=image_uuid,
                position_id=uuid.UUID(position_id),
                type=image_type,
                extension=extension
            )
            db.add(position_image)

        filename = f"{image_uuid}.{extension}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        db.commit()

        flash("Image uploaded successfully.", "success")
        return redirect(request.referrer)
    except (ValueError, TypeError) as e:
        flash("Invalid input. Please check your form data.", "danger")
        return redirect(request.referrer)
    except Exception as e:
        db.rollback()
        flash("An error occurred while uploading the image.", "danger")
        return redirect(request.referrer)
