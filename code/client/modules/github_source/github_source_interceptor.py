import os.path
import spur
import logging

from framework.context import SourceContext
from framework.interceptor import SourceInterceptor
from . import GithubSourceConfig


class GithubSourceInterceptor(SourceInterceptor[GithubSourceConfig]):
    """ Clone a source from remote git repository for pre-build """

    def pre_source(self, context: SourceContext) -> None:
        if self._validate_path(self.config.pre_build_path):
            logging.info('Success: pre_source path validation')
        else:
            logging.error('Failure: pre_source path validation')

    def on_source(self, context: SourceContext) -> None:
        if self._clone_repo():
            logging.info('Success: on_source GitHub repo ' + self.config.git_repo)
        else:
            logging.error('Failure: on_source GitHub repo ' + self.config.git_repo)

    def _validate_path(self, path: str) -> bool:
        is_valid_path = True
        if os.path.isabs(path):
            logging.info('Located ' + path.__name__ + ": " + path)
        else:
            logging.error('Could not locate ' + path.__name__ + ": " + path)
            is_valid_path = False

        return is_valid_path

    def _clone_repo(self) -> bool:
        clone_success = True
        local_shell = spur.LocalShell()

        try:
            local_shell.run(['ssh-add ', self.config.ssh_key_path])
            logging.info('ssh-add succeeded: ' + self.config.ssh_key_path)
        except spur.RunProcessError:
            logging.error('ssh-add failed: ' + self.config.ssh_key_path)
            clone_success = False

        if clone_success:
            try:
                local_shell.run(self.config.cmd_args)
                logging.info('Git clone succeeded:\n' + self.config.git_command)
            except spur.RunProcessError:
                logging.error('Git clone failed:\n' + self.config.git_command)
                clone_success = False

        return clone_success
