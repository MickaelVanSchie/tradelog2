import dotenv
from flask import Flask

from blueprints.app import main_app
from config.database import database
from config.env import ENV

dotenv.load_dotenv()

def create_app():
    dotenv.load_dotenv()
    app = Flask(__name__)
    app.secret_key = ENV.APPLICATION_SECRET
    app.config['SQLALCHEMY_DATABASE_URI'] = ENV.DATABASE_URI
    app.register_blueprint(main_app)
    database.init_app(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        port=ENV.PORT,
        host=ENV.HOST
    )
