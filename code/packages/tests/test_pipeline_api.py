from unittest import TestCase
from typing import List, Mapping, Deque, Dict
from os import environ

from framework.config import ConfigModel, attribute_property
from framework.api.manage_pipelines import ManagePipelines
from framework.server.config import ServerConfig
from framework.interceptor import SourceInterceptor
from framework.context import SourceContext
from framework.pipeline import Pipeline, PipelineManager


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


class TestPipelineAPI(TestCase):
    ...

    def setUp(self):
        self.pipeline_api = ManagePipelines()
        self.pipeline_manager = PipelineManager()

    def test_pipline_api(self):
        #pipe handled with api, pipe2 handled by pipline_manager
        demo_config = DemoConfig('TestConfig')
        demo_intercetor = DemoInterceptor()
        demo_intercetor.config = demo_config

        pipe = self.pipeline_api.create_pipeline("TEST")
        pipe2 = self.pipeline_manager.create_pipeline('TEST2')

        pipe.config = [demo_intercetor]
        pipe2.config = [demo_intercetor]
        #check both pipes exist
        self.assertEqual(pipe.config[0].__class__, pipe2.config[0].__class__)
