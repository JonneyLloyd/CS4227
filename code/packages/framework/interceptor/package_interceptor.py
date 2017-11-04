from abc import abstractmethod
from typing import TypeVar, Generic

from . import ConfigurableInterceptor
from ..context import PackageContext
from ..config import ConfigModel
T = TypeVar('T', bound=ConfigModel)


class PackageInterceptor(ConfigurableInterceptor[T], Generic[T]):

    @abstractmethod
    def pre_package(self, context: PackageContext) -> None:
        ...

    @abstractmethod
    def on_package(self, context: PackageContext) -> None:
        ...
