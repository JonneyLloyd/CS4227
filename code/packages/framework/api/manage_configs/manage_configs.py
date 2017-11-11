from typing import Type, Any, Mapping, Dict, List
from ...config import ConfigModelToSchema
from ...config.config_model_base import ConfigModelBase

class ManageConfigs:

    def get_schema(self, item: ConfigModelBase)-> Mapping[str, Any]:
        return ConfigMapper.convert(item)

    def create_config_model(self, pipeline:str) ->ConfigModelBase:
        #use pipeline_manager to create a config on a pipeline
        ...

    def get_config(self, pipeline:str) -> ConfigModelBase:
        #use pipeline_manager to get a config from pipeline name
        ...

    def get_all_config(self, pipeline:str) -> List[ConfigModelBase]:
        #use pipeline_manager to get all config from pipeline name
        ...

    def delete_config(self, pipeline:str) -> None:
        #use pipeline_manager to delete a config from a pipeline
        ...
