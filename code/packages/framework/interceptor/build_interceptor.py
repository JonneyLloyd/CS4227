from abc import abstractmethod
from typing import TypeVar, Generic
import spur
import logging

from . import ConfigurableInterceptor
from ..context import BuildContext
from ..config import ConfigModel
T = TypeVar('T', bound=ConfigModel)


class BuildInterceptor(ConfigurableInterceptor[T], Generic[T]):

    @abstractmethod
    def pre_build(self, context: BuildContext) -> None:
        ...

    @abstractmethod
    def on_build(self, context: BuildContext) -> None:
        ...

    def remove_existing_build(self, path: str) -> None:
        """ Removes existing builds in build directory """
        local_shell = spur.LocalShell()
        try:
            local_shell.run(['sh', '-c', 'rm -r ' + path])
            logging.info('build_interceptor: Removed existing build')
        except spur.RunProcessError:
            logging.error('build_interceptor: Failed to remove existing build')
