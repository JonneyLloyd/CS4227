from abc import abstractmethod
from typing import TypeVar, Generic
import spur
import logging

from . import ConfigurableInterceptor
from ..context import DeployContext
from ..config import ConfigModel
T = TypeVar('T', bound=ConfigModel)


class DeployInterceptor(ConfigurableInterceptor[T], Generic[T]):

    @abstractmethod
    def pre_deploy(self, context: DeployContext) -> None:
        ...

    @abstractmethod
    def on_deploy(self, context: DeployContext) -> None:
        ...

    def remove_existing_files(self, path: str, is_file: bool) -> None:
        """ Removes existing builds and packages in build directory """
        local_shell = spur.LocalShell()
        if is_file:
            cmd = 'rm '
            type = 'package'
        else:
            cmd = 'rm -r '
            type = 'build'
        try:
            local_shell.run(['sh', '-c', cmd + path])
            logging.info('deploy_interceptor: Removed existing ' + type)
        except spur.RunProcessError:
            logging.error('deploy_interceptor: Failed to remove existing ' + type)
