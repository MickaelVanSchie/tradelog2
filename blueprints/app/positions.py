import uuid
from datetime import datetime

from flask import redirect, url_for, request

from blueprints.app import main_app
from config.database import db
from models import Position


@main_app.post('/create-position')
def create_position():
    entry = float(request.form.get('entry'))
    take_profit = float(request.form.get('take_profit'))
    stop_loss = float(request.form.get('stop_loss'))
    pair = uuid.UUID(request.form.get('pair'))
    reason = request.form.get('reason')
    size = request.form.get('size')

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
