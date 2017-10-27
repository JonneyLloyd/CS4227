from abc import ABC, abstractmethod
from .context_object import ContextObject

class Interceptor(ABC):

    @abstractmethod
    def event_callback(self, context: ContextObject) -> None:
        pass
