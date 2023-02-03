import dotenv
from flask import Flask

from apps.controllers import register_blueprints
from extensions import register_extensions

dotenv.load_dotenv()

from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    register_blueprints(app)

    return app


def create_worker_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)

    return app
