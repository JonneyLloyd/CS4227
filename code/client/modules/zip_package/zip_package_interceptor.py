import os.path
import logging
from shutil import make_archive

from framework.context import PackageContext
from framework.interceptor import PackageInterceptor
from . import ZipPackageConfig
logging.basicConfig(level=logging.INFO)


class ZipPackageInterceptor(PackageInterceptor[ZipPackageConfig]):
    """ Package up build with archive/compression
        Outputs packaged build with package name: build_name.<archive_format> """

    def pre_package(self, context: PackageContext) -> None:
        context.set_state({'pre_package': 'in progress', 'on_package': 'waiting'})
        if self._validate_path(self.config.build_path) and \
           self._validate_path(self.config.package_root):
            self.remove_existing_package(self.config.package_path + '.' + self.config.archive_format)
            logging.info('zip_package_interceptor: Success: pre_package for build: ' + self.config.build_name)
            context.set_state({'pre_package': 'successful', 'on_package': 'waiting'})
        else:
            logging.error('zip_package_interceptor: Failure: pre_package for build: ' + self.config.build_name)
            context.set_state({'pre_package': 'failed', 'on_package': 'waiting'})

    def on_package(self, context: PackageContext) -> None:
        context.set_state({'pre_package': 'successful', 'on_package': 'in progress'})
        if self._archive_format_command(self.config.archive_format):
            logging.info('zip_package_interceptor: Success: on_package for build: ' + self.config.build_name)
            context.set_state({'pre_package': 'successful', 'on_package': 'successful'})
        else:
            logging.error('zip_package_interceptor: Fail: on_package for build: ' + self.config.build_name)
            context.set_state({'pre_package': 'successful', 'on_package': 'failed'})

    def _validate_path(self, path: str) -> bool:
        is_valid_path = True
        if os.path.isdir(path):
            logging.info('zip_package_interceptor: Located path: ' + path)
        else:
            logging.error('zip_package_interceptor: Could not locate path: ' + path)
            is_valid_path = False

        return is_valid_path

    def _archive_format_command(self, format) -> bool:
        found_format = True
        archive_list = [
            'zip',  # compression
            'gztar',  # compression
            'xztar',  # compression
            'tar'  # archive only
        ]
        if format in archive_list:
            self._archive(format)
            logging.info('zip_package_interceptor: Packaged build with format: ' + format)
        else:
            logging.error('zip_package_interceptor: Invalid archive format supplied')
            found_format = False

        return found_format

    def _archive(self, format: str) -> None:
        make_archive(
            self.config.package_path,
            format,
            root_dir=self.config.build_root,
            base_dir=self.config.build_name)
