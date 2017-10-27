import os
from flask import Flask
from .extensions import api


class AppFactory(object):
    @staticmethod
    def create_app(config):
        app = Flask(__name__)
        app.config.from_object(config)
        with app.app_context():
            AppFactory._load_extensions_before(app)
            AppFactory._load_controllers(app)
            AppFactory._load_extensions_after(app)
        return app

    @staticmethod
    def _load_extensions_before(app):
        pass

    @staticmethod
    def _load_controllers(app):
        pass

    @staticmethod
    def _load_extensions_after(app):
        api.init_app(app)
