import os.path
import logging
import spur

from framework.context import SourceContext
from framework.interceptor import SourceInterceptor
from . import RemoteSourceConfig


class RemoteSourceInterceptor(SourceInterceptor[RemoteSourceConfig]):
    """ Copy a remote source to a local directory for pre-build """

    def pre_source(self, context: SourceContext) -> None:
        if self._validate_path(self.config.pre_build_path) and \
           self._validate_path(self.config.ssh_key_path) and \
           self._validate_remote_path(self.config.remote_path):
            logging.info('Success: pre_source for remote path: ' + self.config.remote_path)
        else:
            logging.error('Failure: pre_source for remote path: ' + self.config.remote_path)

    def on_source(self, context: SourceContext) -> None:
        if self._copy_remote_source():
            logging.info('Success: on_source for remote path: ' + self.config.remote_path)
        else:
            logging.error('Fail: on_source for remote path: ' + self.config.remote_path)

    def _validate_path(self, path: str) -> bool:
        is_valid_path = True
        if os.path.isabs(path):
            logging.info('Located ' + path.__name__ + ": " + path)
        else:
            logging.error('Could not locate ' + path.__name__ + ": " + path)
            is_valid_path = False

        return is_valid_path

    def _validate_remote_path(self) -> bool:
        is_valid_path = True
        test_dir_cmd = 'test -d ' + self.config.remote_path
        test_dir_args = test_dir_cmd.split()

        remote_shell = spur.SshShell(
            hostname=self.config.remote_hostname,
            username=self.config.remote_username,
            private_key_file=self.config.ssh_key_path
        )
        try:
            remote_shell.run(test_dir_args)
            logging.info('Located remote source path: ' + self.config.remote_path)
        except spur.RunProcessError:
            logging.error('Could not locate remote source path: ' + self.config.remote_path)
            is_valid_path = False

        return is_valid_path

    def _copy_remote_source(self) -> bool:
        copy_success = True
        scp_args = self.config.scp_command.split()
        local_shell = spur.LocalShell()

        try:
            local_shell.run(scp_args)
            logging.info('Copying remote source succeeded: ' + self.config.scp_command)
        except spur.RunProcessError:
            logging.error('Copying remote source failed: ' + self.config.scp_command)
            copy_success = False

        return copy_success
