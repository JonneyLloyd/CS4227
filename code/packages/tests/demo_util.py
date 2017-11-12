from typing import List, Mapping, Deque, Dict
from os import environ
from framework.config import ConfigModel, attribute_property
from framework.server import PipelineServer, ServerConfig
from framework.interceptor import SourceInterceptor
from framework.context import SourceContext


class DemoConfig(ConfigModel):
    """
    Dummy class for demonstratating arbitrary features of the framework.
    """

    __documentname__ = 'demo'

    def __init__(self, a: str=None) -> None:
        self._a = a

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

class DemoInterceptor(SourceInterceptor[DemoConfig]):
    """
    Dummy class for demonstratating arbitrary features of the framework.
    """

    def pre_source(self, context: SourceContext) -> None:
        print(f"The DemoInterceptor received an event! Config a='{self.config.a}'")

    def on_source(self, context: SourceContext) -> None:
        print(f"The DemoInterceptor received an event! Config a='{self.config.a}'")

class TestConfig(ServerConfig):
    environ['AWS_ACCESS_KEY_ID'] = 'dummy'
    environ['AWS_SECRET_ACCESS_KEY'] = 'dummy'
    AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')
    DYNAMO_ENABLE_LOCAL = True
    DYNAMO_LOCAL_HOST = 'localhost'
    DYNAMO_LOCAL_PORT = 8000
    DYNAMO_TABLES = [
        dict(
            TableName='mementos',
            KeySchema=[dict(AttributeName='type', KeyType='HASH')],
            AttributeDefinitions=[dict(AttributeName='type', AttributeType='S')],
            ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5),
        )
    ]

class DummyConfig(ConfigModel):

    __documentname__ = 'dummy_config'

    def __init__(self):
        self._dummy = None

    @property
    def dummy(self) -> str:
        return self._dummy

    @attribute_property('_dummy')
    def dummy(self) -> str:
        return self._dummy

    @dummy.setter
    def dummy(self, dummy: str) -> None:
        self._dummy = dummy
