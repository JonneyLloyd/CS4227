import os.path
import spur
import logging

from framework.context import SourceContext
from framework.interceptor import SourceInterceptor
from . import GithubSourceConfig


class GithubSourceInterceptor(SourceInterceptor[GithubSourceConfig]):
    """ Clone a source from remote git repository for pre-build """

    def on_source(self, context: SourceContext) -> None:
        source_success = True
        if self._validate_path(self.config.pre_build_path) and \
           self._validate_path(self.config.ssh_key_path):
            logging.info('Success: on_source path validation')
        else:
            logging.error('Failure: on_source path validation')
            source_success = False

        if source_success and self._clone_repo():
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
        ssh_git_cmd = 'eval `ssh-agent`; ssh-add ' + self.config.ssh_key_path + \
                      '; cd ' + self.config.pre_build_path + '; ' + self.config.git_command
        try:
            local_shell.run(['sh', '-c', ssh_git_cmd])
            logging.info('Git clone succeeded: ' + self.config.git_command)
        except spur.RunProcessError:
            logging.error('Git clone failed: ' + self.config.git_command)
            clone_success = False

        return clone_success
