from unittest import TestCase
from os import environ

from framework.context import SourceContext
from framework.interceptor import SourceInterceptor
from framework.config import ConfigModel, attribute_property
from framework.pipeline import Pipeline, PipelineManager
from framework.server import PipelineServer, ServerConfig
from framework.server.app_factory import AppFactory
from framework.store.store_factory import StoreFactory
from .demo_util import DummyConfig, TestConfig, DemoInterceptor

class DummyPipeline(Pipeline):
    ...


class Tests(TestCase):

    def test_database_settings_debug(self):
        config = TestConfig()
        app = AppFactory.create_app(config)

        assert app.config['AWS_ACCESS_KEY_ID'] == environ.get('AWS_ACCESS_KEY_ID')
        assert app.config['AWS_SECRET_ACCESS_KEY'] == environ.get('AWS_SECRET_ACCESS_KEY')
        assert app.config['DYNAMO_ENABLE_LOCAL'] == True
        assert app.config['DYNAMO_LOCAL_HOST'] == 'localhost'
        assert app.config['DYNAMO_LOCAL_PORT'] == 8000
        assert len(app.config['DYNAMO_TABLES']) == 1
"""
    def test_memento_save_restore(self):
        server = PipelineServer(TestConfig())
        server.register_module(DummyConfig, DemoInterceptor)
        store = StoreFactory.create_store()

        dummy_config = DummyConfig()
        dummy_config.dummy = 'random value'
        demo_interceptor = DemoInterceptor()
        demo_interceptor.config = dummy_config

        pipeline_manager = PipelineManager()
        dummy_pipeline = pipeline_manager.create_pipeline('dummy_pipeline')
        dummy_pipeline.config = [demo_interceptor]

        pipeline_memento = dummy_pipeline.create_memento()
        store.save_pipeline('dummy_pipeline', pipeline_memento)
        restored_pipeline_memento = store.restore_pipeline('dummy_pipeline')

        assert pipeline_memento.config[0].config == restored_pipeline_memento.config[0].config

        restored_pipeline = pipeline_manager.create_pipeline('restored_pipeline')
        restored_pipeline.set_memento(restored_pipeline_memento)

        assert dummy_pipeline.config[0].config.__dict__ == restored_pipeline.config[0].config.__dict__

        store.delete_pipeline('dummy_pipeline')
"""
