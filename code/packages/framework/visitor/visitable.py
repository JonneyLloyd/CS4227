from abc import ABC, abstractmethod
from framework.visitor.visitor import Visitor


class Visitable(ABC):

    @abstractmethod
    def accept(self, visitor: Visitor) -> None:
        raise NotImplementedError()
