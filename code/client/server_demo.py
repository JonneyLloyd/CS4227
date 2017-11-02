import os
from os import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.app_factory import AppFactory
from config import Config


def main() -> None:
    server_demo()

def server_demo() -> None:
    app = AppFactory.create_app(Config)
    app.run()

if __name__ == "__main__":
    main()
