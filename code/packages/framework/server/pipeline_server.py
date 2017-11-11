from typing import Type

from flask import Flask
from typing import Tuple

from ..config import ConfigModelBase
from ..interceptor import ConfigurableInterceptor
from ..control import ModuleRegistry
from .config import ServerConfig
from .app_factory import AppFactory


class PipelineServer:

    def __init__(self, config: ServerConfig) -> None:
        self._app = AppFactory.create_app(config)

    @property
    def app(self) -> Flask:
        return self._app

    def start(self) -> None:
        self._app.run()

    def register_module(self, config: Type[ConfigModelBase], interceptor: Type[ConfigurableInterceptor]) -> None:
        ModuleRegistry.register(config, interceptor)

    def get_module(self, name: str) -> Tuple[ConfigModel, ConfigurableInterceptor]:
        return ModuleRegistry.get_module(name)
