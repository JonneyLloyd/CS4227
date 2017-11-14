from framework.config import ConfigModel, attribute_property


class LocalSourceConfig(ConfigModel):

    __documentname__ = 'local_source'

    def __init__(self, source_path: str, pre_build_path: str) -> None:
        """
        Copy source from local source to local directory for pre-build

        Attributes:
            source_path: Absolute path to local source directory
            pre_build_path: Absolute path to directory in which to copy source
        """
        self._source_path = source_path.rstrip('\/')
        self._pre_build_path = pre_build_path.rstrip('\/')

    @attribute_property('source_path')
    def source_path(self) -> str:
        return self._source_path

    @source_path.setter
    def source_path(self, source_path: str) -> None:
        self._source_path = source_path.rstrip('\/')

    @attribute_property('pre_build_path')
    def pre_build_path(self) -> str:
        return self._pre_build_path

    @pre_build_path.setter
    def pre_build_path(self, pre_build_path: str) -> None:
        self._pre_build_path = pre_build_path.rstrip('\/')
