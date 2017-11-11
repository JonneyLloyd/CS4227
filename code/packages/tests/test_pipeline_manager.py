from unittest import TestCase
from os import environ

from framework.interceptor import SourceInterceptor
from framework.server.config import ServerConfig
from framework.config import ConfigModel, attribute_property
from framework.pipeline import Pipeline, PipelineManager
from framework.server import PipelineServer
from framework.context import SourceContext
from framework.config import ConfigMemento
from framework.server.app_factory import AppFactory
from framework.store.store_factory import StoreFactory

from typing import List, Mapping, Deque, Dict


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

    def __init__(self, a: str=None) -> None:
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
    APP_PORT = 5000
    DEBUG = True
    LOG_LEVEL = 'debug'
    DATABASE_URI = ''
    DATABASE_KEY = ''
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

class PipelineManagerTests(TestCase):

    def setUp(self):
        self.pipeline_manager = PipelineManager()

    def test_pipeline_creation_from_memento(self):
        server = PipelineServer(TestConfig())
        server.register_module(DemoConfig, DemoInterceptor)
        store = StoreFactory.create_store()

        demo_config = DemoConfig('Dobby')

        demo_pipeline = self.pipeline_manager.create_pipeline('Dobby')
        demo_pipeline.config = [demo_config]

        memento = demo_pipeline.create_memento()

        demo_pipeline2 = self.pipeline_manager.restore_from_memento('Demo', memento)
        self.assertEqual(demo_pipeline.config[0].__class__, demo_pipeline2.config[0].__class__)
