from abc import abstractmethod
from typing import TypeVar, Generic
import spur
import logging

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

    def remove_existing_package(self, path: str) -> None:
        """ Removes existing packages in package directory """
        local_shell = spur.LocalShell()
        try:
            local_shell.run(['sh', '-c', 'rm ' + path])
            logging.info('package_interceptor: Removed existing package')
        except spur.RunProcessError:
            logging.error('package_interceptor: Failed to remove existing package')
