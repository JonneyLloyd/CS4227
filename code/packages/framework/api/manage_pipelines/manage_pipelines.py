from typing import Type, Any, Mapping, Dict, List
from ...pipeline import Pipeline, PipelineManager
from ...config import ConfigModel

class ManagePipelines(object):
    def __init__(self):
        self.pipeline_manager = PipelineManager()

    def create_pipeline(self, name: str) -> None:
        pipeline = self.pipeline_manager.create_pipeline(name)
        return pipeline

    def execute_pipeline(self, name: str) -> None:
        self.pipeline_manager.execute_pipeline(name)

    def get_all_pipelines(self) -> List[Pipeline]:
        pipelineList = ... # type: List[Pipeline]
        #call 'get all' func in pipeline_manager
        return pipelineList

    def get_pipeline(self, name:str) -> Pipeline:
        #call 'get all' func in pipeline_manager
        pipeline = ... # type: Pipeline
        return pipeline

    def delete_pipeline(self, name:str) -> None:
        ...
        #call delete func in pipeline_manager

    def attach_interceptor(self, name:str, interceptor: 'Interceptor') -> None:
        self.pipeline_manager.attach_interceptor(name, interceptor)

    def create_interceptor(self, name: str, interceptor: 'Interceptor', config: ConfigModel) -> None:
        self.pipeline_manager.create_interceptor(name, interceptor, config)
