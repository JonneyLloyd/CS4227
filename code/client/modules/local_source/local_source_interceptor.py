import os.path
import logging
import spur
from code.client.modules.local_source import SourceInterceptor


class LocalSourceInterceptor(SourceInterceptor):

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

    def on_source(self, context: SourceContext):
        if self.__validate_path(self._pre_build_path) and \
           self.__validate_path(self._source_path):
            if self.__copy_local_source():
                logging.info('Success: Copy local source')
            else:
                logging.error('Fail: Copy local source')

    def __validate_path(self, path: str) -> bool:
        is_valid_path = True
        if os.path.isdir(self._source_path):
            logging.info('Located ' + path.__name__ + ": " + path)
        else:
            logging.error('Could not locate ' + path.__name__ + ": " + path)
            is_valid_path = False

        return is_valid_path

    def __copy_local_source(self) -> bool:
        copy_success = True
        local_shell = spur.LocalShell()

        result = local_shell.run(self._copy_command)
        if result.return_code != 0:
            logging.error('Copying local source failed:\n' + result.stderr_output)
            copy_success = False
        else:
            logging.info('Copying local source succeeded' + result.output)

        return copy_success
