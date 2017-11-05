import os.path
import spur
import logging

from framework.context import SourceContext
from framework.interceptor import SourceInterceptor
from . import GithubSourceConfig


class GithubSourceInterceptor(SourceInterceptor[GithubSourceConfig]):
    def __init__(self, pre_build_path: str, git_user: str, git_repo: str,
                 git_branch: str, ssh_key_path: str) -> None:
        """
        Clone a source from remote git repository for pre-build

        Args:
            pre_build_path: Absolute Path to directory to clone repo into
                            e.g. '/home/deployment/pre_build/'
            git_user: Username of git repo owner
            git_repo: Name of git repository
            git_branch: Branch of repo to clone
            ssh_key_path: Absolute path to SSH private key """
        self._pre_build_path = pre_build_path
        self._git_user = git_user
        self._git_repo = git_repo
        self._git_branch = git_branch
        self._ssh_key_path = ssh_key_path
        self._git_command: str = 'git clone ssh://git@github.com:' + \
                                 self._git_user + "/" + self._git_repo + \
                                 ' -b ' + self._git_branch
        self._cmd_args: list = self._git_command.split()

    def pre_source(self, context: SourceContext) -> None:
        if self._validate_path(self._pre_build_path):
            logging.info('Success: pre_source path validation')
        else:
            logging.error('Failure: pre_source path validation')

    def on_source(self, context: SourceContext) -> None:
        if self._clone_repo():
            logging.info('Success: on_source GitHub repo ' + self._git_repo)
        else:
            logging.error('Failure: on_source GitHub repo ' + self._git_repo)

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
            local_shell.run(['ssh-add ', self._ssh_key_path])
            logging.info('ssh-add succeeded: ' + self._ssh_key_path)
        except spur.RunProcessError:
            logging.error('ssh-add failed: ' + self._ssh_key_path)
            clone_success = False

        if clone_success:
            try:
                local_shell.run(self._cmd_args)
                logging.info('Git clone succeeded:\n' + self._git_command)
            except spur.RunProcessError:
                logging.error('Git clone failed:\n' + self._git_command)
                clone_success = False

        return clone_success
