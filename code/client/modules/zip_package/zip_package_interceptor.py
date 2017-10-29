import os.path
import logging
from shutil import make_archive
from code.client.modules.zip_package import PackageInterceptor


class ZipPackageInterceptor(PackageInterceptor):

    def __init__(self, build_root: str, build_name: str,
                 package_path: str, archive_format: str) -> None:
        """
        Package up build with archive/compression
        Args:
            build_root: Absolute path to root directory of build
                        e.g. '/home/deployment/build_dir/'
            build_name: Name of build e.g. 'python_build_v121'
            package_path: Absolute path to archived package
                          e.g. '/home/deployment/package_dir/zip_package_v121'
            archive_format: Format for archiving/compression e.g. 'zip' """
        self._build_root = build_root
        self._build_name = build_name
        self._package_path = package_path
        self._archive_format = archive_format
        self._build_path = self._build_root + self._build_name

    def on_build(self) -> None:
        if self.__validate_path(self._build_path) and \
           self.__validate_path(self._package_path):

            if self.__archive_format_command(self._archive_format):
                logging.info('Success: Packaged build')
            else:
                logging.error('Fail: Packaging build')

    def __validate_path(self, path: str) -> bool:
        is_valid_path = True
        if os.path.isdir(self._source_path):
            logging.info('Located ' + path.__name__ + ": " + path)
        else:
            logging.error('Could not locate ' + path.__name__ + ": " + path)
            is_valid_path = False

        return is_valid_path

    def __archive_format_command(self, x) -> bool:
        found_format = True
        archive_dict = {
            'zip': self.__archive('zip'),  # compression
            'gztar': self.__archive('gztar'),  # compression
            'xztar': self.__archive('xztar'),  # compression
            'tar': self.__archive('tar')  # archive only
        }
        if x in archive_dict.keys():
            archive_dict[x]
        else:
            logging.error('Invalid archive format supplied')
            found_format = False

        return found_format

    def __archive(self, format: str) -> None:
        make_archive(
            self._package_path,
            format,
            root_dir=self._build_root,
            base_dir=self._build_name)

