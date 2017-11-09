from typing import List
from framework.config import ConfigMemento


class PipelineMemento(object):

    @property
    def config(self) -> List[ConfigMemento]:
        return self._config

    @config.setter
    def config(self, value: List[ConfigMemento]) -> None:
        self._config = value
