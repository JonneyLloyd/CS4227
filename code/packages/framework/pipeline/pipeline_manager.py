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
        def attach_interceptor(self, name: str, interceptor: 'Interceptor') -> None:
            dispatcher = self._pipelines[name].source_dispatcher
            dispatcher.register(interceptor)

        def create_interceptor(self, name: str, Interceptor: 'Interceptor', config: ConfigModel) -> None:
             interceptor = Interceptor()
             interceptor.config = config
             self.attach_interceptor(name, config)

        def add_config_to_pipeline(self, name:str, config: ConfigModel, idx: int) -> None:
            pipeline = self._pipelines.get(name, None)
            if pipeline:
                pipeline.configs.insert(idx, config)

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

        def execute_pipeline(self, name: str) -> None:
            if not self._pipeline_threads.get(name, None):
                self._pipeline_threads[name] = Thread(target=self._pipelines[name].execute)
            self._pipeline_threads[name].start()

    # The PipelineManager is a singleton that manages multiple Pipelines.
    instance = None
    def __init__(self):
        if not PipelineManager.instance:
            PipelineManager.instance = PipelineManager.__PipelineManager()

    def __getattr__(self, name):
        return getattr(self.instance, name)
