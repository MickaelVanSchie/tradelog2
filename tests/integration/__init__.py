from flask import app


def test_app_runs():
    flask_app = app

    with flask_app.test_