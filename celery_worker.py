# celery_worker.py
from ig_api_db_client import create_app

app = create_app()
celery = app.celery

if __name__ == '__main__':
    celery.start()
