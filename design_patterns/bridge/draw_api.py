from abc import ABC, abstractmethod


class DrawAPI(ABC):

    @abstractmethod
    def draw_circle(self, radius: int, x: int, y: int) -> None:
        pass
