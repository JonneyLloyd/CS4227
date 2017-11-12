from typing import Type, Any, Mapping, Dict, List
from ...config import ConfigModelToSchema
from ...config.config_model_base import ConfigModelBase
#import pipeline_manager

class ManageConfigs:

    def get_schema(self, item: ConfigModelBase) -> Mapping[str, Any]:
        return ConfigModelToSchema.convert(item)

    def create_config_model(self, pipeline:str) -> ConfigModelBase:
        config = ... # type: ConfigModelBase
        #use pipeline_manager to create a config on a pipeline
        return config

    def get_config(self, pipeline:str, index: int) -> ConfigModelBase:
        config = ... # type: ConfigModelBase
        #use pipeline_manager to get a config from pipeline name
        return config

    def get_all_configs(self, pipeline:str) -> List[ConfigModelBase]:
        configList = ... # type: List[ConfigModelBase]
        #use pipeline_manager to get all config from pipeline name
        return configList

    def delete_config(self, pipeline:str, index: int) -> None:
        #use pipeline_manager to delete a config from a pipeline
        ...
