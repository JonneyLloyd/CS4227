from .factory import Factory
from .shape import Shape
from .rectangle import Rectangle
from .square import Square


class ShapeFactory(Factory):

    def get_shape(self, shape: str) -> Shape:
        if shape.upper() == "RECTANGLE":
            return Rectangle()
        elif shape.upper() == "SQUARE":
            return Square()
