import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "crsd-secret-key")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "crsd.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = "crsd-dev-secret-key"
