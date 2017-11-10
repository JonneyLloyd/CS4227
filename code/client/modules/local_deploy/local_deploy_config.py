from framework.config import ConfigModel, attribute_property


class LocalDeployConfig(ConfigModel):

    __documentname__ = 'local_deploy'

    def __init__(self, package_path: str, build_name: str,
                 deploy_root: str, script_list: list, packaged: bool) -> None:
        """
        Deploy an app locally - extract if packaged, run series of scripts

        Attributes:
            package_path: Absolute path to packaged build (path to build if not packaged)
            build_name: Name of build that is packaged (tail of packaged_path without file
                        format extension)
            deploy_root: Absolute path to root directory for deployments (If build is not
                         packaged, build will be located inside this directory by default)
            script_list: List of absolute paths of scripts to execute during deployment
                         The paths to scripts should be identical across multiple hosts
                         e.g. '/deployment/build_hello_world/app/hello_world.py'
            packaged: Boolean flag - set to true if build is packaged and set to false
                      if not packaged (flag not used for remote deploy)
        """
        self._package_path = package_path
        self._build_name = build_name
        self._deploy_root = deploy_root
        self._script_list = script_list
        self._packaged = packaged
        self._unpacked_build = self._deploy_root.rstrip('\/') + '/' + self._build_name
        self._python_path = self._unpacked_build + '/venv/bin/python3'

    @attribute_property('package_path')
    def package_path(self) -> str:
        return self._package_path

    @package_path.setter
    def package_path(self, package_path: str) -> None:
        self._package_path = package_path

    @attribute_property('build_name')
    def build_name(self) -> str:
        return self._build_name

    @build_name.setter
    def build_name(self, build_name: str) -> None:
        self._build_name = build_name

    @attribute_property('deploy_root')
    def deploy_root(self) -> str:
        return self._deploy_root

    @deploy_root.setter
    def deploy_root(self, deploy_root: str) -> None:
        self._deploy_root = deploy_root

    @attribute_property('script_list')
    def script_list(self) -> list:
        return self._script_list

    @script_list.setter
    def script_list(self, script_list: list) -> None:
        self._script_list = script_list

    @attribute_property('packaged')
    def packaged(self) -> bool:
        return self._packaged

    @packaged.setter
    def packaged(self, packaged: bool) -> None:
        self._packaged = packaged

    @attribute_property('unpacked_build')
    def unpacked_build(self) -> str:
        return self._unpacked_build

    @attribute_property('python_path')
    def python_path(self) -> str:
        return self._python_path
