from abc import ABC, abstractmethod
from typing import List

from framework.pipeline.pipline_memento import PipelineMemento


class DocumentStore(ABC):

    @abstractmethod
    def save(self, name: str, _list: List[dict]) -> None:
        ...

    @abstractmethod
    def restore(self, name: str) -> List[dict]:
        ...

    @abstractmethod
    def delete(self, name: str) -> None:
        ...
