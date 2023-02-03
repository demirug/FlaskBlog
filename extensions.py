from celery import Celery
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

login_manager = LoginManager()
db = SQLAlchemy()
mail = Mail()
celery = Celery()


def register_extensions(app):
    login_manager.init_app(app)
    mail.init_app(app)

    celery.conf.update(app.config["CELERY_CONFIG"])

    with app.app_context():
        db.init_app(app)
        db.create_all()

    celery.config_from_object(app.config)
