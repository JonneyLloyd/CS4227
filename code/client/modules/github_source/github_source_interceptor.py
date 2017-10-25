import os


class GithubSourceInterceptor:

    """ Input: Path to clone repo into
               Url of git repo
               Branch of repo to pull
               SSH username
               SSH password """
    def __init__(self, localPath: str, git_url: str, git_branch: str,
                 ssh_user_host: str, ssh_password: str):
        self.localPath = localPath
        self.git_url = git_url
        self.git_branch = git_branch
        self.git_command: str = 'git clone ' + self.git_url + ' -b ' + self.git_branch
        self.ssh_user_host = ssh_user_host
        self.ssh_pass_command: str = 'sshpass -f ' + self.ssh_pass_file + ' ssh ' + self.ssh_user_host
        self.ssh_password = ssh_password

    def validateLocalPath(self) -> bool:
        errorMsg = 'ERROR: Could not locate local path: '
        isValidPath = True
        if os.path.isdir(self.localPath):
            print('Located source path: ' + self.localPath)
        else:
            errorMsg += self.localPath
            print(errorMsg)
            isValidPath = False
        return isValidPath

    def cloneRepo(self) -> None:
        os.system(self.ssh_pass_command)
        os.chdir(self.localPath)
        os.system(self.git_command)

        # handle errors TODO



