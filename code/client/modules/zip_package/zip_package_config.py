from framework.config import ConfigModel, attribute_property


class ZipPackageConfig(ConfigModel):

    __documentname__ = 'zip_package'

    def __init__(self, build_root: str, build_name: str,
                 package_root: str, archive_format: str) -> None:
        """
        Package up build with archive/compression
        Outputs packaged build with name build_name.<archive_format>

        Attributes:
            build_root: Absolute path to root directory of build
                        e.g. '/home/deployment/build_dir/'
            build_name: Name of build e.g. 'python_build_v121'
            package_root: Absolute path to root directory of packaged builds
                          e.g. '/home/deployment/package_dir'
            archive_format: Format for archiving/compression e.g. 'zip' """
        self._build_root = build_root
        self._build_name = build_name
        self._package_root = package_root
        self._archive_format = archive_format
        self._package_path = package_root.rstrip('\/') + '/' + build_name
        self._build_path = self._build_root.rstrip('\/') + '/' + self._build_name

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

    @attribute_property('package_root')
    def package_root(self) -> str:
        return self._package_root

    @package_root.setter
    def package_root(self, package_root: str) -> None:
        self._package_root = package_root

    @attribute_property('archive_format')
    def archive_format(self) -> str:
        return self._archive_format

    @archive_format.setter
    def archive_format(self, archive_format: str) -> None:
        self._archive_format = archive_format

    @attribute_property('package_path')
    def package_path(self) -> str:
        return self._package_path

    @attribute_property('build_path')
    def build_path(self) -> str:
        return self._build_path
