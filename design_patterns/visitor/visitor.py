from abc import ABCMeta, abstractmethod


class Element(object, metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        pass


class ConcreteElement(Element):
    def accept(self, visitor):
        visitor.visit(self)

class Visitor(metaclass=ABCMeta):
    @abstractmethod
    def visit(self, element):
        pass


class ConcreteVisitor(Visitor):
    def visit(self, element):
        print(f'Visiting element.')
