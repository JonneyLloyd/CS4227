import os.path
import logging
import spur

from framework.context import SourceContext
from framework.interceptor import SourceInterceptor
from . import RemoteSourceConfig
logging.basicConfig(level=logging.INFO)


class RemoteSourceInterceptor(SourceInterceptor[RemoteSourceConfig]):
    """ Copy a remote source to a local directory for pre-build """

    def on_source(self, context: SourceContext) -> None:
        context.set_state({'on_source': 'in progress'})
        source_success = True
        if self._validate_path(self.config.pre_build_path, False) and \
           self._validate_path(self.config.ssh_key_path, True) and \
           self._validate_remote_path():
            logging.info('remote_source_interceptor: Success: on_source remote path validation: ' + self.config.remote_path)
        else:
            logging.error('remote_source_interceptor: Failure: on_source remote path validation: ' + self.config.remote_path)

        if source_success:
            self.remove_existing_source(self.config.pre_build_path + '/' + os.path.basename(self.config.remote_path))
            if self._copy_remote_source():
                logging.info('remote_source_interceptor: Success: on_source for remote path: ' + self.config.remote_path)
                context.set_state({'on_source': 'successful'})
            else:
                logging.error('remote_source_interceptor: Fail: on_source for remote path: ' + self.config.remote_path)
                context.set_state({'on_source': 'failed'})

    def _validate_path(self, path: str, is_file: bool) -> bool:
        """ The is_file flag determines if validating a file or directory path """
        is_valid_path = True
        if is_file and not os.path.isfile(path):
            is_valid_path = False
        elif not is_file and not os.path.isdir(path):
            is_valid_path = False
        if is_valid_path:
            logging.info('remote_source_interceptor: Located path: ' + path)
        else:
            logging.error('remote_source_interceptor: Could not locate path: ' + path)

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
            logging.info('remote_source_interceptor: Located remote source path: ' + self.config.remote_path)
        except spur.RunProcessError:
            logging.error('remote_source_interceptor: Could not locate remote source path: ' + self.config.remote_path)
            is_valid_path = False

        return is_valid_path

    def _copy_remote_source(self) -> bool:
        copy_success = True
        scp_args = self.config.scp_command.split()
        local_shell = spur.LocalShell()

        try:
            local_shell.run(scp_args)
            logging.info('remote_source_interceptor: Copying remote source succeeded: ' + self.config.scp_command)
        except spur.RunProcessError:
            logging.error('remote_source_interceptor: Copying remote source failed: ' + self.config.scp_command)
            copy_success = False

        return copy_success
