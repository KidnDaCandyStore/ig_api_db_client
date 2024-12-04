# celery.py
from celery import Celery
from ig_api_db_client.config import Config

def make_celery():
    celery = Celery(
        'ig_api_db_client',
        broker=Config.CELERY_BROKER_URL,
        backend=Config.CELERY_RESULT_BACKEND
    )
    celery.conf.update(
        broker_url=Config.CELERY_BROKER_URL,
        result_backend=Config.CELERY_RESULT_BACKEND,
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
    )
    
    # Autodiscover tasks from all registered Django app configs.
    celery.autodiscover_tasks(['ig_api_db_client.tasks'])
    
    return celery

celery = make_celery()
