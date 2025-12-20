import uuid

from flask import redirect, url_for, request

from blueprints.app import main_app
from config.database import db
from models import Position


@main_app.post('/create-position')
def create_position():
    print(request.form)

    position = Position(
        id=uuid.uuid4(),
        type="long"
    )

    db.add(position)

    return redirect(url_for('main_app.index'))