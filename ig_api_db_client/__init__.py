# __init__.py
import logging

logging.basicConfig(level=logging.DEBUG)

from flask import Flask
from .config import Config
from .database import db
from .instagram_client import InstagramClient
from .celery_app import make_celery  # Import make_celery function

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize Database
    db.init_app(app)

    # Initialize Instagram client
    InstagramClient.get_instance(
        username=Config.INSTAGRAM_USERNAME,
        password=Config.INSTAGRAM_PASSWORD,
        secret_key=Config.SECRET_KEY
    )

    # Initialize Celery
    celery = make_celery(app)
    app.celery = celery  # Optionally attach celery to app

    # Register Blueprints
    with app.app_context():
        from .routes import api
        app.register_blueprint(api, url_prefix='/api')
        db.create_all()

    return app
