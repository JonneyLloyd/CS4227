from app.app_factory import AppFactory
from config import Config

if __name__ == "__main__":
    app = AppFactory.create_app(Config)
    app.run()
