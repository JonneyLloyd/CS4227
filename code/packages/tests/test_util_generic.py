import unittest
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Dict

from framework.util.generic import GenericABC


class Example(ABC):

    @abstractmethod
    def get(self) -> str:
        ...

class ExampleX(Example):

    def get(self) -> str:
        return 'X'

class ExampleY(Example):

    def get(self) -> str:
        return 'Y'


# Generic Factory Method
T = TypeVar('T', bound=Example)
class A(GenericABC, Generic[T]):

    def create(self) -> T:
        clazz: Type = self._get_generic_type(T)
        return clazz()

# Subtypes of the Generic Factory
class B(A[ExampleX]):
    ...

U = TypeVar('U', bound=Example)
class C(A[U], Generic[U]):
    ...

class D(C[ExampleY]):
    ...


V = TypeVar('V', bound=Example)
W = TypeVar('W', bound=Example)
class E(GenericABC, Generic[V, W]):

    def create_first(self) -> V:
        clazz: Type = self._get_generic_type(V)
        return clazz()

    def create_second(self) -> W:
        clazz: Type = self._get_generic_type(W)
        return clazz()

class F(GenericABC, Generic[W, V]):

    def create_first(self) -> W:
        clazz: Type = self._get_generic_type(W)
        return clazz()

    def create_second(self) -> V:
        clazz: Type = self._get_generic_type(V)
        return clazz()


class TestGenericABC(unittest.TestCase):

    def test_generic_create_inherited(self):
        self.assertEqual(B().create().get(), 'X')

    def test_generic_create_double_inherited(self):
        self.assertEqual(D().create().get(), 'Y')

    def test_generic_create_parameterised(self):
        self.assertEqual(A[ExampleX]().create().get(), 'X')
        self.assertEqual(A[ExampleY]().create().get(), 'Y')

    def test_generic_create_inherited_parameterised(self):
        self.assertEqual(C[ExampleX]().create().get(), 'X')
        self.assertEqual(C[ExampleY]().create().get(), 'Y')

    def test_generic_create_multiple(self):
        e = E[ExampleX, ExampleY]()
        self.assertEqual(e.create_first().get(), 'X')
        self.assertEqual(e.create_second().get(), 'Y')
        e = E[ExampleY, ExampleX]()
        self.assertEqual(e.create_first().get(), 'Y')
        self.assertEqual(e.create_second().get(), 'X')

    def test_generic_create_multiple_switched(self):
        f = F[ExampleX, ExampleY]()
        self.assertEqual(f.create_first().get(), 'X')
        self.assertEqual(f.create_second().get(), 'Y')
