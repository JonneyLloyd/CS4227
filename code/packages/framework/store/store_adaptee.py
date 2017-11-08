from abc import ABC, abstractmethod
from typing import List

from framework.config import ConfigMemento
from framework.control import ModuleRegistry
from framework.pipeline.pipline_memento import PipelineMemento
from framework.store.document_store import DocumentStore


class StoreAdaptee(ABC):

    def __init__(self, store: DocumentStore) -> None:
        self._store = store

    @property
    def store(self) -> DocumentStore:
        return self._store

    def save_pipeline(self, pipeline_memento: PipelineMemento) -> None:
        config_memento_list = self._extract_config_memento_list(pipeline_memento)
        self.store.save(pipeline_memento.name, config_memento_list)

    def restore_pipeline(self, name: str) -> PipelineMemento:
        config_mementos = self._instantiate_config_mementos(self.store.restore(name))
        pipeline_memento = PipelineMemento()
        pipeline_memento.name = name
        pipeline_memento.config = config_mementos
        return pipeline_memento

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

    @abstractmethod
    def save(self, memento: PipelineMemento) -> None:
        ...

    @abstractmethod
    def restore(self, name: str) -> PipelineMemento:
        ...

    @abstractmethod
    def delete(self, name: str) -> None:
        ...
