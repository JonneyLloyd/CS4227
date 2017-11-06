import os


class ServerConfig:
    APP_NAME = 'Pipeline'
    APP_PORT = 80
    SECRET_KEY = os.urandom(12)
    DEBUG = False
    LOG_LEVEL = 'info'

    DATABASE_URI = None
    DATABASE_KEY = None
