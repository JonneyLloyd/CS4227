import os.path
import logging
import spur
from framework.interceptor import SourceInterceptor


class RemoteSourceInterceptor(SourceInterceptor):

    def __init__(self, remote_path: str, pre_build_path: str, remote_username: str,
                 remote_hostname: str, ssh_key_path: str) -> None:
        """
        Copy a remote source to a local directory for pre-build
        Args:
            remote_path: Absolute path to remote source directory
            pre_build_path: Absolute path to local directory in which to copy remote source
            remote_username: Username on remote host
            remote_hostname: Hostname of remote host
            ssh_key_path: Absolute path to SSH private key
        """
        self._remote_path = remote_path
        self._pre_build_path = pre_build_path
        self._remote_username = remote_username
        self._remote_hostname = remote_hostname
        self._ssh_key_path = ssh_key_path
        self._scp_command = 'scp -r ' + self._remote_username + '@' + self._remote_hostname \
                            + ':' + self._remote_path + " " + self._pre_build_path

    def on_source(self, context: SourceContext):
        if self._validate_path(self._pre_build_path) and \
           self._validate_path(self._ssh_key_path) and \
           self._validate_remote_path(self._remote_path):
            if self._copy_remote_source():
                logging.info('Success: Copy remote source')
            else:
                logging.error('Fail: Copy remote source')

    def _validate_path(self, path: str) -> bool:
        is_valid_path = True
        if os.path.isdir(self._source_path):
            logging.info('Located ' + path.__name__ + ": " + path)
        else:
            logging.error('Could not locate ' + path.__name__ + ": " + path)
            is_valid_path = False

        return is_valid_path

    def _validate_remote_path(self) -> bool:
        is_valid_path = True
        remote_shell = spur.SshShell(
            hostname=self._remote_hostname,
            username=self._remote_username,
            private_key_file=self._ssh_key_path
        )
        result = remote_shell.run('test -d ' + self._remote_path)
        if result.return_code != 0:
            logging.error('Could not locate remote source path: ' + self._remote_path)
            is_valid_path = False
        else:
            logging.info('Located remote source path: ' + self._remote_path)

        return is_valid_path

    def _copy_remote_source(self) -> bool:
        copy_success = True
        local_shell = spur.LocalShell()

        result = local_shell.run(self._scp_command)
        if result.return_code != 0:
            logging.error('Copying remote source failed:\n' + result.stderr_output)
            copy_success = False
        else:
            logging.info('Copying remote source succeeded:\n' + result.output)

        return copy_success
