from design_patterns.abstract_factory import ShapeFactory
from design_patterns.bridge import Circle, RedCircle, GreenCircle


def main() -> None:
    factory_demo()
    bridge_demo()


def factory_demo():
    factory = ShapeFactory()
    rectangle = factory.get_shape("rectangle")
    square = factory.get_shape("square")

    rectangle.draw()
    square.draw()


def bridge_demo():
    red_circle = Circle(10, 100, 100, RedCircle())
    green_circle = Circle(10, 100, 100, GreenCircle())

    red_circle.draw()
    green_circle.draw()


if __name__ == '__main__':
    main()
