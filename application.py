import dotenv
from celery import Celery
from flask import Flask
from flask_admin import Admin
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from apps.controllers import register_blueprints

dotenv.load_dotenv()

from config import Config

login_manager = LoginManager()
db = SQLAlchemy()
mail = Mail()
celery = Celery()
ckeditor = CKEditor()
migrate = Migrate()
admin = Admin(name='flask-blog')


def create_app():
    app = create_base_app()
    register_blueprints(app)
    with app.app_context():
        db.create_all()

    migrate.init_app(app, db)
    admin.init_app(app)
    return app


def create_base_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)

    celery.conf.update(app.config["CELERY_CONFIG"])
    celery.config_from_object(app.config)

    return app
