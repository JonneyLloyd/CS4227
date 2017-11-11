from typing import Type, Dict, Tuple

from ..config import ConfigModelBase
from ..interceptor import ConfigurableInterceptor


class ModuleRegistry:

    _registry: Dict[str, Tuple[ConfigModelBase, ConfigurableInterceptor]] = {}

    @staticmethod
    def register(config: Type[ConfigModelBase], interceptor: Type[ConfigurableInterceptor]) -> None:
        ModuleRegistry._registry[config.__documentname__] = config, interceptor

    @staticmethod
    def get_module(name: str) -> Tuple[ConfigModelBase, ConfigurableInterceptor]:
        return ModuleRegistry._registry[name]
