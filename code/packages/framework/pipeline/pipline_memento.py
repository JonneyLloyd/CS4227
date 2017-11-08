from typing import List
from framework.config import ConfigMemento


class PipelineMemento:

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def config(self) -> List[ConfigMemento]:
        return self._config

    @config.setter
    def config(self, value: List[ConfigMemento]) -> None:
        self._config = value
