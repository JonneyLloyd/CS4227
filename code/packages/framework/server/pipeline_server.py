from typing import Type

from ..config import ConfigModel
from ..interceptor import ConfigurableInterceptor
from ..control import ModuleRegistry
from .config import ServerConfig
from .app_factory import AppFactory


class PipelineServer:

    def __init__(self, config: ServerConfig) -> None:
        self._app = AppFactory.create_app(config)

    def start(self) -> None:
        self._app.run()

    def register_module(self, config: Type[ConfigModel], interceptor: Type[ConfigurableInterceptor]) -> None:
        ModuleRegistry.register(config, interceptor)
