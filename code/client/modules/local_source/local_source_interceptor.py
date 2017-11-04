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
        self._copy_command = 'cp -r ' + self._source_path + ' ' + self._pre_build_path

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
            logging.error('Fail: on_source for local source')

    def _validate_path(self, path: str) -> bool:
        is_valid_path = True
        if os.path.isdir(self._source_path):
            logging.info('Located ' + path.__name__ + ": " + path)
        else:
            logging.error('Could not locate ' + path.__name__ + ": " + path)
            is_valid_path = False

        return is_valid_path

    def _copy_local_source(self) -> bool:
        copy_success = True
        local_shell = spur.LocalShell()

        result = local_shell.run(self._copy_command)
        if result.return_code != 0:
            logging.error('Copying local source failed:\n' + result.stderr_output)
            copy_success = False
        else:
            logging.info('Copying local source succeeded\n' + result.output)

        return copy_success
