# __init__.py
import logging
from flask import Flask
from .config import Config
from .database import db
from .instagram_client import InstagramClient

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

    # Register Blueprints
    with app.app_context():
        from .routes import api
        app.register_blueprint(api, url_prefix='/api')
        db.create_all()

    return app
