from typing import Type, Any, Mapping, Dict, List
from ...pipeline import Pipeline
#import pipeline_manager




class ManagePipelines(object):
    ...

    def create_pipeline(self, name: str) -> None:
        pipeline = ... # type: Pipeline
        #call create_pipeline in pipeline_manager
        return pipeline

    def execute_pipeline(self, name: str) -> None:
        ...
        #call execute_pipelinee in pipeline_manager

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
