from flask import Flask

from blueprints.app import main_app

app = Flask(__name__)
app.register_blueprint(main_app)

app.run()