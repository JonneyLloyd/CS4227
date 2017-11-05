import os.path
import logging
from shutil import make_archive
from framework.context import PackageContext
from framework.interceptor import PackageInterceptor

from . import ZipPackageConfig


class ZipPackageInterceptor(PackageInterceptor[ZipPackageConfig]):
    """ Package up build with archive/compression """

    def pre_package(self, context: PackageContext) -> None:
        if self._validate_path(self.config.build_path) and \
           self._validate_path(self.config.package_path):
            logging.info('Success: pre_package for build: ' + self.config.build_name)
        else:
            logging.error('Failure: pre_package for build: ' + self.config.build_name)

    def on_package(self, context: PackageContext) -> None:
        if self._archive_format_command(self.config.archive_format):
            logging.info('Success: on_package for build: ' + self.config.build_name)
        else:
            logging.error('Fail: on_package for build: ' + self.config.build_name)

    def _validate_path(self, path: str) -> bool:
        is_valid_path = True
        if os.path.isabs(path):
            logging.info('Located ' + path.__name__ + ": " + path)
        else:
            logging.error('Could not locate ' + path.__name__ + ": " + path)
            is_valid_path = False

        return is_valid_path

    def _archive_format_command(self, format) -> bool:
        found_format = True
        archive_list = {
            'zip',  # compression
            'gztar',  # compression
            'xztar',  # compression
            'tar'  # archive only
        }
        if format in archive_list:
            self._archive(format)
            logging.info('Packaged build with format: ' + format)
        else:
            logging.error('Invalid archive format supplied')
            found_format = False

        return found_format

    def _archive(self, format: str) -> None:
        make_archive(
            self.config.package_path,
            format,
            root_dir=self.config.build_root,
            base_dir=self.config.build_name)
