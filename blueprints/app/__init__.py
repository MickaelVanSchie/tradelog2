from flask import Blueprint, render_template

from config.database import db
from models import Position

main_app = Blueprint('main_app', __name__, template_folder='templates')


@main_app.route('/')
def index():
    positions = db.query(Position).order_by(Position.created.desc()).all()
    return render_template('overview.html', positions=positions)