import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your_secret_key"
    INSTANCE_PATH = os.path.join(os.path.dirname(__file__), 'instance')
    DATABASE = os.path.join(INSTANCE_PATH, 'tiny.db')