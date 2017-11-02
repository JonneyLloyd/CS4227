from abc import ABC, abstractmethod
from framework.json import JsonRequest
from framework.util.overload import overload


class JsonVisitor(ABC):

    @overload
    @abstractmethod
    def visit(self, visitable: JsonRequest) -> str:
        ...

