from framework.config import ConfigModel, attribute_property


class PythonBuildConfig(ConfigModel):

    __documentname__ = 'python_build'

    def __init__(self, pre_build_path: str, build_root: str, build_name: str) -> None:
        """
        Build a python application - create virtual environment and install dependencies
        See PythonBuildInterceptor docstrings for more information

        Attributes:
            pre_build_path: Absolute path to local directory containing app source files
            build_root: Absolute path to directory containing finished build
            build_name: Name of build, directory in build_root will be called this
        """
        self._pre_build_path = pre_build_path.rstrip('\/')
        self._build_root = build_root
        self._build_name = build_name
        self._build_path = build_root.rstrip('\/') + '/' + build_name
        self._venv_path = self._build_path + '/venv'

    @attribute_property('pre_build_path')
    def pre_build_path(self) -> str:
        return self._pre_build_path

    @pre_build_path.setter
    def pre_build_path(self, pre_build_path: str) -> None:
        self._pre_build_path = pre_build_path.rstrip('\/')

    @attribute_property('build_root')
    def build_root(self) -> str:
        return self._build_root

    @build_root.setter
    def build_root(self, build_root: str) -> None:
        self._build_root = build_root

    @attribute_property('build_name')
    def build_name(self) -> str:
        return self._build_name

    @build_name.setter
    def build_name(self, build_name: str) -> None:
        self._build_name = build_name

    @attribute_property('build_path')
    def build_path(self) -> str:
        return self._build_path

    @attribute_property('venv_path')
    def venv_path(self) -> str:
        return self._venv_path
