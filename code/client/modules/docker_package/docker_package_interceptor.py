from framework.context import PackageContext
from framework.interceptor import PackageInterceptor

from . import DockerPackageConfig


class DockerPackageInterceptor(PackageInterceptor[DockerPackageConfig]):

    def on_package(self, context: PackageContext) -> None:
        ...
