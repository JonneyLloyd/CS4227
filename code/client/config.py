from framework.server.config import ServerConfig


class ProdConfig(ServerConfig):
    DATABASE_URI = ''
    DATABASE_KEY = ''


class DevConfig(ServerConfig):
    APP_PORT = 8080
    DEBUG = True
    LOG_LEVEL = 'verbose'
    DATABASE_URI = ''
    DATABASE_KEY = ''


class TestConfig(ServerConfig):
    APP_PORT = 5000
    DEBUG = True
    LOG_LEVEL = 'debug'
    DATABASE_URI = ''
    DATABASE_KEY = ''
