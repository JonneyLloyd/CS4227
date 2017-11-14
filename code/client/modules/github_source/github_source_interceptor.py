import os.path
import spur
import logging

from framework.context import SourceContext
from framework.interceptor import SourceInterceptor
from . import GithubSourceConfig
logging.basicConfig(level=logging.INFO)


class GithubSourceInterceptor(SourceInterceptor[GithubSourceConfig]):
    """ Clone a source from remote git repository for pre-build """

    def on_source(self, context: SourceContext) -> None:
        context.set_state({'on_source': 'waiting'})
        source_success = True
        if self._validate_path(self.config.pre_build_path, False) and \
           self._validate_path(self.config.ssh_key_path, True):
            logging.info('github_source_interceptor: Success: on_source path validation')
        else:
            logging.error('github_source_interceptor: Failure: on_source path validation')
            source_success = False

        if source_success:
            self.remove_existing_source(self.config.pre_build_path + '/' + self.config.git_repo)
            if self._clone_repo():
                logging.info('github_source_interceptor: Success: on_source GitHub repo ' + self.config.git_repo)
                context.set_state({'on_source': 'successful'})
            else:
                logging.error('github_source_interceptor: Failure: on_source GitHub repo ' + self.config.git_repo)
                context.set_state({'on_source': 'failed'})

    def _validate_path(self, path: str, is_file: bool) -> bool:
        """ The is_file flag determines if validating a file or directory path """
        is_valid_path = True
        if is_file and not os.path.isfile(path):
            is_valid_path = False
        elif not is_file and not os.path.isdir(path):
            is_valid_path = False
        if is_valid_path:
            logging.info('github_source_interceptor: Located path: ' + path)
        else:
            logging.error('github_source_interceptor: Could not locate path: ' + path)

        return is_valid_path

    def _clone_repo(self) -> bool:
        clone_success = True
        local_shell = spur.LocalShell()
        ssh_git_cmd = 'eval `ssh-agent`; ssh-add ' + self.config.ssh_key_path + \
                      '; cd ' + self.config.pre_build_path + '; ' + self.config.git_command
        try:
            local_shell.run(['sh', '-c', ssh_git_cmd])
            logging.info('github_source_interceptor: Git clone succeeded: ' + self.config.git_command)
        except spur.RunProcessError:
            logging.error('github_source_interceptor: Git clone failed: ' + self.config.git_command)
            clone_success = False

        return clone_success
