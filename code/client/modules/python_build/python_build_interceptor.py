from framework.interceptor import BuildInterceptor
from framework.context import BuildContext


class PythonBuildInterceptor(BuildInterceptor):

    def on_build(self, context: BuildContext):
        ...
