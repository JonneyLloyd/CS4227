from typing import Type, Dict, Tuple

from ..config import ConfigModel
from ..interceptor import ConfigurableInterceptor


class ModuleRegistry:

    _registry: Dict[str, Tuple[ConfigModel, ConfigurableInterceptor]] = {}

    @staticmethod
    def register(config: Type[ConfigModel], interceptor: Type[ConfigurableInterceptor]) -> None:
        ModuleRegistry._registry[config.__documentname__] = config, interceptor

    @staticmethod
    def get_module(name: str) -> Tuple[ConfigModel, ConfigurableInterceptor]:
        return ModuleRegistry._registry[name]
