import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
    INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')
    SECRET_KEY = os.getenv('SECRET_KEY')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    # Ensure REDIS_URL includes database number
    if REDIS_URL.count('/') == 2:
        REDIS_URL += '/0'

    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
