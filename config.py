import os

app_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = 'qwertyuiopasdfghjklmnbvcxz'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 1024 * 1024


class DevelopementConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///textdb.db'
