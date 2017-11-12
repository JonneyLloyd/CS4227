from abc import ABC, abstractmethod
from typing import List

from framework.config import ConfigMemento
from framework.control import ModuleRegistry
from framework.pipeline.pipeline_memento import PipelineMemento


class DocumentStore(ABC):

    @abstractmethod
    def _save(self, name: str, _list: List[dict]) -> None:
        ...

    @abstractmethod
    def _restore(self, name: str) -> List[dict]:
        ...

    @abstractmethod
    def _delete(self, name: str) -> None:
        ...

    def save_pipeline(self, name: str, pipeline_memento: PipelineMemento) -> None:
        config_memento_list = self._extract_config_memento_list(pipeline_memento)
        self._save(name, config_memento_list)

    def restore_pipeline(self, name: str) -> PipelineMemento:
        config_mementos = self._instantiate_config_mementos(self._restore(name))
        pipeline_memento = PipelineMemento()
        pipeline_memento.config = config_mementos
        return pipeline_memento

    def delete_pipeline(self, name: str) -> None:
        self._delete(name)

    def _extract_config_memento_list(self, pipeline_memento: PipelineMemento) -> List[dict]:
        config_mementos = pipeline_memento.config
        _list = []
        for config_memento in config_mementos:
            _list.append(config_memento.config)
        return _list

    def _instantiate_config_mementos(self, config_list: List[dict]) -> List[ConfigMemento]:
        config_mementos = []
        for obj in config_list:
            config_name = list(obj.keys())[0]
            instances = ModuleRegistry.get_module(config_name)
            config_model = instances[0]()

            for key in config_model.__dict__:
                config_model.__dict__[key] = obj[config_name][key]

            config_mementos.append(config_model.create_memento())
        return config_mementos
