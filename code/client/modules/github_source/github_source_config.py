from framework.config import ConfigModel, attribute_property


class GithubSourceConfig(ConfigModel):

    __documentname__ = 'github_source'

    def __init__(self, pre_build_path: str, git_user: str, git_repo: str,
                 git_branch: str, ssh_key_path: str) -> None:
        """
        Clone a source from remote git repository for pre-build

        Attributes:
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
        self._git_command: str = 'git clone git@github.com:' + self._git_user + "/" + \
                                 self._git_repo + '.git -b ' + self._git_branch

    @attribute_property('pre_build_path')
    def pre_build_path(self) -> str:
        return self._pre_build_path

    @pre_build_path.setter
    def pre_build_path(self, pre_build_path: str) -> None:
        self._pre_build_path = pre_build_path

    @attribute_property('git_user')
    def git_user(self) -> str:
        return self._git_user

    @git_user.setter
    def git_user(self, git_user: str) -> None:
        self._git_user = git_user

    @attribute_property('git_repo')
    def git_repo(self) -> str:
        return self._git_repo

    @git_repo.setter
    def git_repo(self, git_repo: str) -> None:
        self._git_repo = git_repo

    @attribute_property('git_branch')
    def git_branch(self) -> str:
        return self._git_branch

    @git_branch.setter
    def git_branch(self, git_branch: str) -> None:
        self._git_branch = git_branch

    @attribute_property('ssh_key_path')
    def ssh_key_path(self) -> str:
        return self._ssh_key_path

    @ssh_key_path.setter
    def ssh_key_path(self, ssh_key_path: str) -> None:
        self._ssh_key_path = ssh_key_path
