from framework.context import PackageContext
from framework.interceptor import PackageInterceptor


class DockerPackageInterceptor(PackageInterceptor):

    def on_package(self, context: PackageContext):
        ...
