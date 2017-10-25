import os

class BaseConfig(object):
    SECRET_KEY = os.urandom(12)

class Config(BaseConfig):
    DEBUG = True
