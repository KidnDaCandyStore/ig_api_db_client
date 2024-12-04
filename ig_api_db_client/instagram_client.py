import os
import logging
import threading
import pyotp
import json
from instagrapi import Client, exceptions

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
            self.login()
            self.initialized = True

    def login(self):
        try:
            logging.info('Attempting to login to Instagram...')
            self.cl.login(self.username, self.password)
            logging.info("Logged in to Instagram successfully.")
        except exceptions.TwoFactorRequired as e:
            logging.info("Two-factor authentication required. Providing verification code.")
            totp = pyotp.TOTP(self.secret_key)
            verification_code = totp.now()
            try:
                # Use the code received via TOTP
                self.cl.login(self.username, self.password, verification_code=verification_code)
                logging.info("Two-factor authentication successful.")
            except Exception as e:
                logging.error(f"Failed to complete two-factor authentication: {e}")
                raise
        except exceptions.ChallengeRequired as e:
            logging.error("Challenge required. Manual intervention needed.")
            raise
        except Exception as e:
            logging.error(f"Failed to login to Instagram: {e}")
            raise

    @classmethod
    def get_instance(cls, username=None, password=None, secret_key=None):
        if cls._instance is None:
            if not all([username, password, secret_key]):
                raise ValueError("InstagramClient not initialized. Provide username, password, and secret_key.")
            cls(username, password, secret_key)
        return cls._instance

    def get_client(self):
        return self.cl
