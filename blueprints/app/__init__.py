from flask import Blueprint

main_app = Blueprint('main_app', __name__)


@main_app.route('/')
def index():
    return 'Hello World!'