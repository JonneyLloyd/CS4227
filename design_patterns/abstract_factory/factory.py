from abc import ABC, abstractmethod
from ..bridge.shape import Shape


class Factory(ABC):

    @abstractmethod
    def get_shape(self, shape: str) -> Shape:
        pass
