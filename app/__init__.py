from flask import Flask
from celery import Celery

def make_flask_app():
    app = Flask(__name__)
    app.config['CELERY_BROKER_URL'] = 'redis://host.docker.internal:6379/0'  # Connect to Redis running on host
    app.config['CELERY_RESULT_BACKEND'] = 'redis://host.docker.internal:6379/0'
    return app

def make_celery(app=None):
    app = app or make_flask_app()
    celery = Celery(app.import_name,
                    broker=app.config['CELERY_BROKER_URL'],
                    backend=app.config['CELERY_RESULT_BACKEND'])
    celery.conf.update(app.config)
    return celery
