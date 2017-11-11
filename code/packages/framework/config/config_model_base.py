from abc import ABC, abstractmethod
from typing import Type, Dict

from ..config import ConfigMemento


class ConfigModelBase(ABC):

    @abstractmethod
    def set_memento(self, memento: ConfigMemento) -> None:
        ...

    @abstractmethod
    def create_memento(self) -> ConfigMemento:
        ...

    @classmethod
    @abstractmethod
    def create_schema(cls) -> Dict:
        ...
