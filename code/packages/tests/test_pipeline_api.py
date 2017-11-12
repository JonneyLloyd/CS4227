from unittest import TestCase
from typing import List, Mapping, Deque, Dict
from os import environ

from framework.config import ConfigModel, attribute_property
from framework.api.manage_pipelines import ManagePipelines
#from framework.rest_api.rest_manage_pipelines import PipelineListAPI
from framework.server.config import ServerConfig
from framework.interceptor import SourceInterceptor
from framework.context import SourceContext
from framework.pipeline import Pipeline, PipelineManager
from .demo_util import DemoConfig, DemoInterceptor


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
