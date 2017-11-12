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

from .demo_util import DemoConfigChild, DemoConfig, DemoInterceptor, TestConfig

from typing import List, Mapping, Deque, Dict


class PipelineManagerTests(TestCase):

    def setUp(self):
        self.pipeline_manager = PipelineManager()

    def test_pipeline_creation_from_memento(self):
        server = PipelineServer(TestConfig())
        server.register_module(DemoConfig, DemoInterceptor)
        store = StoreFactory.create_store()

        demo_config = DemoConfig('Dobby')
        demo_intercetor = DemoInterceptor()
        demo_intercetor.config = demo_config

        demo_pipeline = self.pipeline_manager.create_pipeline('Dobby')
        demo_pipeline.config = [demo_intercetor]

        memento = demo_pipeline.create_memento()

        demo_pipeline2 = self.pipeline_manager.restore_from_memento('Demo', memento)
        self.assertEqual(demo_pipeline.config[0].__class__, demo_pipeline2.config[0].__class__)
