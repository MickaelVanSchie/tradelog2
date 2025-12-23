from flask import Blueprint, render_template

from config.database import db
from models import Position
from models.pair import Pair

main_app = Blueprint('main_app', __name__, template_folder='templates', static_folder='static', url_prefix='/')

from .positions import create_position

@main_app.route('/')
def index() -> str:
    positions = db.query(Position).order_by(Position.created.asc()).all()
    pairs = db.query(Pair).all()

    return render_template('overview.html', positions=positions, pairs=pairs)