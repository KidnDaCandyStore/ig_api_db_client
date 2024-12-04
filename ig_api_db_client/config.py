import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
    INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')
    SECRET_KEY = os.getenv('SECRET_KEY')
    broker_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    result_backend = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
