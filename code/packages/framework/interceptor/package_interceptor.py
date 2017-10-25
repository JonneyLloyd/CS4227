from abc import abstractmethod

from . import ConfigurableInterceptor
from ..context import PackageContext


class PackageInterceptor(ConfigurableInterceptor):

    @abstractmethod
    def on_package(self, context: PackageContext) -> None:
        ...
