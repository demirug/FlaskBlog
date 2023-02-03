import dotenv
from celery import Celery
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from apps.controllers import register_blueprints

dotenv.load_dotenv()

from config import Config

login_manager = LoginManager()
db = SQLAlchemy()
mail = Mail()
celery = Celery()


def create_app():
    app = create_base_app()
    register_blueprints(app)

    with app.app_context():
        db.create_all()

    return app


def create_base_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)
    mail.init_app(app)
    db.init_app(app)

    celery.conf.update(app.config["CELERY_CONFIG"])
    celery.config_from_object(app.config)

    return app
