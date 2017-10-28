from code.client.modules.docker_package import PackageInterceptor


class DockerPackageInterceptor(PackageInterceptor):

    def on_package(self, context: PackageContext):
        ...
