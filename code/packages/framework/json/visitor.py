from abc import ABC, abstractmethod
from framework.util.overload import overload


class Visitor(ABC):

    @overload
    @abstractmethod
    def visit(self, visitable: 'JsonRequest') -> str:
        ...

