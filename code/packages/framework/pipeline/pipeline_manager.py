from threading import Thread

from ..pipeline import Pipeline, Configs


class PipelineManager(object):
    class __PipelineManager(object):
        def __init__(self):
            self._pipelines = {}
            self._pipeline_threads = {}

        # Attach an inteceptor to a named pipeline
        def attach_interceptor(self, name, interceptor):
            dispatcher = self._pipelines[name].source_dispatcher
            dispatcher.register(interceptor)

        def create_interceptor(self):
            '''The user can create their own interceptor
            which knows about its configs. Else we restore
            from  a memento.'''
            pass

        # Create a pipeline with a name - probably needs to be something better
        def create_pipeline(self, name: str) -> Pipeline:
            if not self._pipelines.get(name, None):
                self._pipelines[name] = Pipeline()
            return self._pipelines[name]

        # Restore / create a pipeline from a Momento
        def restore_from_memento(self, name):
            pipeline = self.create_pipeline(name)
            # memento = retrieve from DB using name
            # pipeline.restore_from_memento(memento)

        # Anytime we execute the pipeline we should be executing on its own thread.
        # This allows multiple pipelines to be run at once.
        def execute_pipeline(self, name: str) -> None:
            if not self._pipeline_threads.get(name, None):
                self._pipeline_threads[name] = Thread(target=self._pipelines[name].execute)
            self._pipeline_threads[name].start()

        def get_pipeline_info(self, name: str) -> None:
            pass

    # The PipelineManager is a singleton that manages multiple Pipelines.
    instance = None
    def __init__(self):
        if not PipelineManager.instance:
            PipelineManager.instance = PipelineManager.__PipelineManager()

    def __getattr__(self, name):
        return getattr(self.instance, name)
