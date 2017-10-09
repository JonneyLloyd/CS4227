
from abc import ABC, abstractmethod
class ContextObject(ABC):

    @abstractmethod
    def set_value(self) -> None:
        pass

    @abstractmethod
    def get_value(self) -> None:
        pass

    @abstractmethod
    def consume_service(self) -> None:
        pass
