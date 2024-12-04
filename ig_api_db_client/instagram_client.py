# instagram_client.py
import os
import logging
import threading
import pyotp
import json
from instagrapi import Client, exceptions
import redis

class InstagramClient:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(InstagramClient, cls).__new__(cls)
        return cls._instance

    def __init__(self, username, password, secret_key):
        if not hasattr(self, 'initialized'):
            self.cl = Client()
            self.username = username
            self.password = password
            self.secret_key = secret_key
            # Initialize Redis client
            self.redis_client = redis.Redis.from_url(os.getenv('REDIS_URL'))
            self.session_key = f'IG_SESSION_{self.username}'
            self.login()
            self.initialized = True

    def login(self):
        try:
            session_data = self.redis_client.get(self.session_key)
            if session_data:
                logging.info('Loading settings from Redis')
                self.cl.set_settings(json.loads(session_data))
                self.cl.login(self.username, self.password)
                logging.info('Logged in using saved settings')
            else:
                logging.info('Logging into Instagram...')
                self.cl.login(self.username, self.password)
                logging.info("Logged in to Instagram successfully.")
                logging.info('Saving settings to Redis')
                session_json = json.dumps(self.cl.get_settings())
                self.redis_client.set(self.session_key, session_json)
        except exceptions.TwoFactorRequired:
            logging.info("Two-factor authentication required. Providing verification code.")
            totp = pyotp.TOTP(self.secret_key)
            verification_code = totp.now()
            try:
                self.cl.login(self.username, self.password, verification_code=verification_code)
                logging.info("Two-factor authentication successful.")
                logging.info('Saving settings to Redis')
                session_json = json.dumps(self.cl.get_settings())
                self.redis_client.set(self.session_key, session_json)
            except Exception as e:
                logging.error(f"Failed to complete two-factor authentication: {e}")
                raise
        except exceptions.ChallengeRequired as e:
            logging.error("Challenge required. Manual intervention needed.")
            raise
        except Exception as e:
            logging.error(f"Failed to login to Instagram: {e}")
            raise
