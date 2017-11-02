import unittest
from typing import List, Mapping, Deque, Dict
from framework.config import ConfigModel, ConfigMemento, attribute_property


class ChildConfig(ConfigModel):
    """
    Dummy class for demonstratating arbitrary features of the framework.
    """

    def __init__(self) -> None:
        self._numbers = []

    @attribute_property('numbers', required=False)
    def numbers(self) -> List[int]:
        return self._numbers

    @numbers.setter
    def l(self, numbers: List[int]) -> None:
        self._numbers = numbers


class ParentConfig(ConfigModel):

    __documentname__ = 'parent'

    def __init__(self) -> None:
        self._a = None
        self._child = ChildConfig()

    @attribute_property('child')
    def child(self) -> ChildConfig:
        return self._child

    @child.setter
    def child(self, child: ChildConfig) -> None:
        self._child = child

    @attribute_property('amazing')
    def a(self) -> str:
        return self._a

    @a.setter
    def a(self, a: str) -> None:
        self._a = a



class TestConfigModel(unittest.TestCase):

    def test_create_memento(self):
        c = ChildConfig()
        c.numbers = [1, 2, 3]
        memento = c.create_memento()
        self.assertEqual(memento.config, {'child_config': {'numbers': [1, 2, 3]}})

    def test_create_memento_nested(self):
        p = ParentConfig()
        p.a = 'word'
        p.child = ChildConfig()
        p.child.numbers = [1, 2, 3]
        memento = p.create_memento()
        self.assertEqual(memento.config, {'parent': {'child': {'numbers': [1, 2, 3]}, 'amazing': 'word'}})

    def test_set_memento(self):
        memento = ConfigMemento()
        memento.config = {'child_config': {'numbers': [1, 2, 3]}}
        c = ChildConfig()
        c.set_memento(memento)
        self.assertEqual(c.create_memento().config, memento.config)

    def test_set_memento_nested(self):
        memento = ConfigMemento()
        memento.config = {'parent': {'child': {'numbers': [1, 2, 3]}, 'amazing': 'word'}}
        p = ParentConfig()
        p.set_memento(memento)
        self.assertEqual(p.create_memento().config, memento.config)
