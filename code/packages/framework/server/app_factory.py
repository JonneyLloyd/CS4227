import os
from flask import Flask

from .config import ServerConfig
from .extensions import api


class AppFactory(object):
    @staticmethod
    def create_app(config: ServerConfig):
        app = Flask(__name__)
        app.config.from_object(config)
        with app.app_context():
            AppFactory._load_extensions_before(app)
            AppFactory._load_controllers(app)
            AppFactory._load_extensions_after(app)
        return app

    @staticmethod
    def _load_extensions_before(app: Flask) -> None:
        pass

    @staticmethod
    def _load_controllers(app: Flask) -> None:
        pass

    @staticmethod
    def _load_extensions_after(app: Flask) -> None:
        api.init_app(app)
