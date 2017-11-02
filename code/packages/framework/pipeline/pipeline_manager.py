from threading import Thread

from ..pipeline import Pipeline, Configs

class PipelineManager(object):
    class __PipelineManager(object):
        def __init__(self):
            self._pipelines = {}
            self._pipeline_threads = {}

        # Create a pipeline with a name - probably needs to be something better
        def create_pipeline(self, name: str, configs: Configs) -> Pipeline:
            if not self._pipelines.get(name, None):
                self._pipelines[name] = Pipeline(configs)
            return self._pipelines[name]

        # Anytime we execute the pipeline we should be executing on its own thread.
        # This allows multiple pipelines to be run at once.
        def execute_pipeline(self, name: str) -> None:
            if not self._pipeline_threads.get(name, None):
                self._pipeline_threads[name] = Thread(target=self._pipelines[name].execute)
            self._pipeline_threads[name].start()

        def get_pipeline_info(self, name: str) -> None:
            ...

    # The PipelineManager is a singleton that manages multiple Pipelines.
    instance = None
    def __init__(self):
        if not PipelineManager.instance:
            PipelineManager.instance = PipelineManager.__PipelineManager()

    def __getattr__(self, name):
        return getattr(self.instance, name)
