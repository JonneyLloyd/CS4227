from abc import ABCMeta, abstractmethod


class Graphic(object, metaclass=ABCMeta):
    @abstractmethod
    def print(self) -> None:
        raise NotImplementedError()


class CompositeGraphic(Graphic):
    def __init__(self):
        self.graphics = []

    def print(self) -> None:
        for graphic in self.graphics:
            graphic.print()

    def add(self, graphic: Graphic) -> None:
        self.graphics.append(graphic)

    def remove(self, graphic: Graphic) -> None:
        self.graphics.remove(graphic)


class Ellipse(Graphic):
    def __init__(self, name):
        self.name = name

    def print(self):
        print("Ellipse:", self.name)
