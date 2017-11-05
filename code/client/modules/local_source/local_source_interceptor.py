import os.path
import logging
import spur

from framework.context import SourceContext
from framework.interceptor import SourceInterceptor
from . import LocalSourceConfig


class LocalSourceInterceptor(SourceInterceptor[LocalSourceConfig]):

    def __init__(self, source_path: str, pre_build_path: str) -> None:
        """
        Copy source from local source to local directory for pre-build

        Args:
            source_path: Absolute path to local source directory
            pre_build_path: Absolute path to directory in which to copy source
        """
        self._source_path = source_path
        self._pre_build_path = pre_build_path

    def pre_source(self, context: SourceContext) -> None:
        if self._validate_path(self._pre_build_path) and \
           self._validate_path(self._source_path):
            logging.info('Success: pre_source path validation')
        else:
            logging.error('Failure: pre_source path validation')

    def on_source(self, context: SourceContext) -> None:
        if self._copy_local_source():
            logging.info('Success: on_source for local source')
        else:
            logging.error('Failure: on_source for local source')

    def _validate_path(self, path: str) -> bool:
        is_valid_path = True
        if os.path.isabs(path):
            logging.info('Located ' + path.__name__ + ": " + path)
        else:
            logging.error('Could not locate ' + path.__name__ + ": " + path)
            is_valid_path = False

        return is_valid_path

    def _copy_local_source(self) -> bool:
        copy_success = True
        copy_command = 'cp -r ' + self._source_path + ' ' + self._pre_build_path
        copy_args = self._copy_command.split()
        local_shell = spur.LocalShell()
        try:
            local_shell.run(copy_args)
            logging.info('Copying local source succeeded: ' + copy_command)
        except spur.RunProcessError:
            logging.error('Copying local source failed: ' + copy_command)
            copy_success = False

        return copy_success
