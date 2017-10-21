from abc import ABC, abstractmethod
from framework.json import Visitor


class Visitable(ABC):

    @abstractmethod
    def accept(self, visitor: Visitor) -> None:
        ...
