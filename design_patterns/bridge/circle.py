from .shape import Shape
from .draw_api import DrawAPI


class Circle(Shape):

    def __init__(self, radius: int, x: int, y: int, draw_api: DrawAPI):
        super().__init__(draw_api)
        self.radius = radius
        self.x = x
        self.y = y

    def draw(self) -> None:
        self.draw_api.draw_circle(self.radius, self.x, self.y)
