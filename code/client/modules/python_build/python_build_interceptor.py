from framework.interceptor import BuildInterceptor
from framework.context import BuildContext

from . import PythonBuildConfig


class PythonBuildInterceptor(BuildInterceptor[PythonBuildConfig]):

    def on_build(self, context: BuildContext):
        ...
