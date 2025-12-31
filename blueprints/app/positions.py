import uuid
from datetime import datetime

from flask import redirect, url_for, request, flash

from blueprints.app import main_app
from blueprints.exceptions.position_store import PositionStoreException
from config.database import db
from models import Position


def store_position(entry, take_profit, stop_loss, pair, reason, size):
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
def create_position():
    try:
        entry = float(request.form.get('entry'))
        take_profit = float(request.form.get('take_profit'))
        stop_loss = float(request.form.get('stop_loss'))
        pair = uuid.UUID(request.form.get('pair'))
        reason = request.form.get('reason')
        size = request.form.get('size')

        store_position(entry, take_profit, stop_loss, pair, reason, size)

        return redirect('/')
    except (ValueError, TypeError):
        flash("Invalid input. Please ensure all fields are filled correctly.", "danger")
        return redirect(request.referrer)
    except PositionStoreException:
        flash("An error occurred while storing your position. Please try again later.", "danger")
        return redirect(request.referrer)
