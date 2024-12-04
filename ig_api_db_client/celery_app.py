# celery_app.py
from celery import Celery
from .config import Config

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['broker_url'],
        backend=app.config['result_backend'],
        include=['ig_api_db_client.tasks']
    )
    celery.conf.update(
        broker_url=app.config['broker_url'],
        result_backend=app.config['result_backend'],
        worker_log_level='INFO',  # Set the desired logging level
        # Include other necessary Celery configurations
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
