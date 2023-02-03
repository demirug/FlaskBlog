import os


class Config:
    DEBUG = os.getenv("DEBUG")
    SECRET_KEY = os.getenv("SECRET_KEY")

    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TLS = True
    MAIL_DEBUG = False

    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")

    CELERY_CONFIG = {
        'broker_url': f'redis://{REDIS_HOST}:{REDIS_PORT}/0',
        'result_backend': f'redis://{REDIS_HOST}:{REDIS_PORT}/0',
        'accept_content': ['application/json'],
        'task_serializer': 'json',
        'result_serializer': 'json'
    }

    SQLALCHEMY_DATABASE_URI = 'sqlite:///flask.db'

    INDEX_VIEW = 'blog.list'
