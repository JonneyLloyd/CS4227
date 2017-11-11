from threading import Thread

from ..pipeline import Pipeline, ConfigMementoList
from ..util import overload
from ..config import ConfigModel

class PipelineManager(object):
    class __PipelineManager(object):
        def __init__(self):
            self._pipelines = {}
            self._pipeline_threads = {}

        # Attach an inteceptor to a named pipeline
        def attach_interceptor(self, name: str, interceptor: 'Interceptor'):
            dispatcher = self._pipelines[name].source_dispatcher
            dispatcher.register(interceptor)

        @overload
        def create_interceptor(self, Interceptor: 'Interceptor', config: ConfigModel):
            interceptor = Interceptor()
            interceptor.config = config
            return interceptor

        @overload
        def create_interceptor(self, name: str, Interceptor: 'Interceptor', config: ConfigModel):
             interceptor = self.create_interceptor(Interceptor, config)
             self.attach_interceptor(name, config)

        def add_config_to_pipeline(self, name:str, config: ConfigModel, idx: int):
            pipeline = self._pipelines.get(name, None)
            if pipeline:
                pipeline.configs.insert(idx, config)
            return pipeline

        # Create a pipeline with a name
        def create_pipeline(self, name: str) -> Pipeline:
            if not self._pipelines.get(name, None):
                self._pipelines[name] = Pipeline()
            return self._pipelines[name]

        # Restore / create a pipeline from a Momento
        def restore_from_memento(self, name, memento) -> Pipeline:
            pipeline = self.create_pipeline(name)
            pipeline.set_memento(memento)
            return pipeline

        # Anytime we execute the pipeline we should be executing on its own thread.
        # This allows multiple pipelines to be run at once.
        def execute_pipeline(self, name: str) -> None:
            self._pipelines[name].execute()

    # The PipelineManager is a singleton that manages multiple Pipelines.
    instance = None
    def __init__(self):
        if not PipelineManager.instance:
            PipelineManager.instance = PipelineManager.__PipelineManager()

    def __getattr__(self, name):
        return getattr(self.instance, name)
