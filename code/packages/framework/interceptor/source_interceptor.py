from abc import abstractmethod
from typing import TypeVar, Generic
import spur
import logging

from . import ConfigurableInterceptor
from ..context import SourceContext
from ..config import ConfigModel
T = TypeVar('T', bound=ConfigModel)


class SourceInterceptor(ConfigurableInterceptor[T], Generic[T]):

    @abstractmethod
    def on_source(self, context: SourceContext) -> None:
        ...

    def remove_existing_source(self, path: str) -> None:
        """ Removes existing sources in pre build directory """
        local_shell = spur.LocalShell()
        try:
            local_shell.run(['sh', '-c', 'rm -r ' + path])
            logging.info('source_interceptor: Removed existing source')
        except spur.RunProcessError:
            logging.error('source_interceptor: Failed to remove existing source')
