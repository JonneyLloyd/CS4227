from typing import Type, Any, Mapping, Dict, List
from ...pipeline import Pipeline
#import pipeline_manager




class ManagePipelines(object):
    ...

    def create_pipeline(self, name: str) ->None:
        ...
        #call create_pipeline in pipeline_manager

    def execute_pipeline(self, name: str) -> None:
        ...
        #call execute_pipelinee in pipeline_manager

    def get_all_pipelines(self) -> List[Pipeline]:
        ...

    def get_pipeline(self, name:str) -> Pipeline:
        ...

    def delete_pipeline(self, name:str) -> None:
        ...
