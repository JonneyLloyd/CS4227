from framework.interceptor import BuildInterceptor


class PythonBuildInterceptor(BuildInterceptor):

    def on_build(self, context: BuildContext):
        ...
