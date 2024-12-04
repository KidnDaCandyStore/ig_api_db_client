from celery import Celery
from .config import Config

def make_celery(app):
    celery = Celery(
        app.import_name,
        include=['ig_api_db_client.tasks']
    )
    # Update Celery configuration with Flask configuration
    celery.conf.update(
        broker_url=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND'],
        # You can add other Celery configuration options here
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
