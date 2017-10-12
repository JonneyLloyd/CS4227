from design_patterns.abstract_factory import ShapeFactory
from design_patterns.bridge import Circle, RedCircle, GreenCircle
from design_patterns.interceptor import Dispatcher, ConcreteInterceptor, ConcreteContext
from design_patterns.memento import Originator
from design_patterns.composite import Ellipse, CompositeGraphic
from design_patterns.state import ConcreteContext
from design_patterns.visitor import ConcreteElement, ConcreteVisitor

def main() -> None:
    factory_demo()
    bridge_demo()
    interceptor_demo()
    memento_demo()
    composite_demo()
    state_demo()
    visitor_demo()


def factory_demo() -> None:
    factory = ShapeFactory()
    rectangle = factory.get_shape("rectangle")
    square = factory.get_shape("square")

    rectangle.draw()
    square.draw()


def bridge_demo() -> None:
    red_circle = Circle(10, 100, 100, RedCircle())
    green_circle = Circle(10, 100, 100, GreenCircle())

    red_circle.draw()
    green_circle.draw()

def interceptor_demo():
    #framework side
    dispatcher = Dispatcher()
    context = ConcreteContext()

    #client side
    interceptor = ConcreteInterceptor()
    dispatcher.register(interceptor)

    #framework side
    dispatcher.callback(context)

def memento_demo() -> None:
    saved_states = []
    originator = Originator()

    originator.set("State1")
    originator.set("State2")
    saved_states.append(originator.create_memento())

    originator.set("State3")
    originator.set("State4")
    originator.restore_from_memento(saved_states[0])

def composite_demo() -> None:
    ellipse1 = Ellipse("1")
    ellipse2 = Ellipse("2")
    ellipse3 = Ellipse("3")
    ellipse4 = Ellipse("4")

    graphic = CompositeGraphic()
    graphic1 = CompositeGraphic()
    graphic2 = CompositeGraphic()

    graphic1.add(ellipse1)
    graphic1.add(ellipse2)
    graphic1.add(ellipse3)

    graphic2.add(ellipse4)

    graphic.add(graphic1)
    graphic.add(graphic2)

    graphic.print()

def state_demo() -> None:
    context = ConcreteContext()
    context.run()
    context.run()

def visitor_demo() -> None:
    element = ConcreteElement()
    visitor = ConcreteVisitor()
    element.accept(visitor)

if __name__ == '__main__':
    main()
