from framework.config import ConfigModel, attribute_property


class RemoteSourceConfig(ConfigModel):

    __documentname__ = 'remote_source'

    def __init__(self, remote_path: str, pre_build_path: str, remote_username: str,
                 remote_hostname: str, ssh_key_path: str) -> None:
        """
        Copy a remote source to a local directory for pre-build

        Attributes:
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

    @attribute_property('remote_path')
    def remote_path(self) -> str:
        return self._remote_path

    @remote_path.setter
    def remote_path(self, remote_path: str) -> None:
        self._remote_path = remote_path

    @attribute_property('pre_build_path')
    def pre_build_path(self) -> str:
        return self._pre_build_path

    @pre_build_path.setter
    def pre_build_path(self, pre_build_path: str) -> None:
        self._pre_build_path = pre_build_path

    @attribute_property('remote_username')
    def remote_username(self) -> str:
        return self._remote_username

    @remote_username.setter
    def remote_username(self, remote_username: str) -> None:
        self._remote_username = remote_username

    @attribute_property('remote_hostname')
    def remote_hostname(self) -> str:
        return self._remote_hostname

    @remote_hostname.setter
    def remote_hostname(self, remote_hostname: str) -> None:
        self._remote_hostname = remote_hostname

    @attribute_property('ssh_key_path')
    def ssh_key_path(self) -> str:
        return self._ssh_key_path

    @ssh_key_path.setter
    def ssh_key_path(self, ssh_key_path: str) -> None:
        self._ssh_key_path = ssh_key_path

    @attribute_property('scp_command')
    def scp_command(self) -> str:
        return self._scp_command
