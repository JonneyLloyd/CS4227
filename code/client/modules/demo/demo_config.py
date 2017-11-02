from typing import List, Mapping, Deque, Dict
from framework.config import ConfigModel, attribute_property


class DemoConfigChild(ConfigModel):
    """
    Dummy class for demonstratating arbitrary features of the framework.
    """

    def __init__(self, a: int=0, b: int=42, l: List[int]=[1,2,3]) -> None:
        self._a = a
        self._b = b
        self._l = l

    @attribute_property('number')
    def a(self) -> str:
        return self._a

    @a.setter
    def a(self, a: str) -> None:
        self._a = a

    @attribute_property('magic_number', required=False)
    def b(self) -> str:
        return self._b

    @b.setter
    def b(self, b: str) -> None:
        self._b = b

    @attribute_property('more_numbers', required=False)
    def l(self) -> List[int]:
        return self._l

    @l.setter
    def l(self, l: List[int]) -> None:
        self._l = l


class DemoConfig(ConfigModel):
    """
    Dummy class for demonstratating arbitrary features of the framework.
    """

    __documentname__ = 'demo'

    def __init__(self, a: str=None, b: str=None) -> None:
        self._a = a
        self._b = b
        self._s = DemoConfigChild(7)
        self._ss = [DemoConfigChild(1), DemoConfigChild(2)]

    @attribute_property('child')
    def s(self) -> DemoConfigChild:
        return self._s

    @s.setter
    def s(self, s: DemoConfigChild) -> None:
        self._s = s

    @attribute_property('children')
    def ss(self) -> List[DemoConfigChild]:
        return self._ss

    @ss.setter
    def ss(self, ss: List[DemoConfigChild]) -> None:
        self._ss = ss

    @attribute_property('amazing')
    def a(self) -> str:
        return self._a

    @a.setter
    def a(self, a: str) -> None:
        self._a = a

    @attribute_property('brilliant', required=False)
    def b(self) -> str:
        return self._b

    @b.setter
    def b(self, b: str) -> None:
        self._b = b
