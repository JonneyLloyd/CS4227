from abc import ABC, abstractmethod
from .draw_api import DrawAPI


class Shape(ABC):

    def __init__(self, draw_api: DrawAPI):
        self.draw_api = draw_api

    @abstractmethod
    def draw(self) -> None:
        pass
