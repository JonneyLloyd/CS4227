from abc import ABC
from typing import List

from framework.config import ConfigMemento, attribute_property
from framework.pipeline.pipline_memento import PipelineMemento


class PipelineBase(ABC):

    @property
    def config(self) -> List[ConfigMemento]:
        return self._config

    @attribute_property('_config')
    def config(self) -> List[ConfigMemento]:
        return self._config

    @config.setter
    def config(self, config: List[ConfigMemento]) -> None:
        self._config = config

    def set_memento(self, memento: PipelineMemento) -> None:
        self.config = memento.config

    def create_memento(self) -> PipelineMemento:
        memento = PipelineMemento()
        memento.name = self.__class__.__name__
        memento.config = self.config
        return memento
