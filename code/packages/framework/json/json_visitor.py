from abc import ABC, abstractmethod
from framework.json import JsonRequest
from framework.util.overload import overload


class JsonVisitor(ABC):

    @abstractmethod
    @overload
    def visit(self, visitable: JsonRequest) -> str:
        ...

