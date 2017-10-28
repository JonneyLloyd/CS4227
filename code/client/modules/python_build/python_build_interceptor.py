from code.client.modules.python_build import BuildInterceptor


class PythonBuildInterceptor(BuildInterceptor):

    def on_build(self, context: BuildContext):
        ...
