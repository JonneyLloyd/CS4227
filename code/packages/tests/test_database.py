from unittest import TestCase
from os import environ

from framework.interceptor import StorageInterceptor
from framework.config import ConfigModel, attribute_property
from framework.pipeline import Pipeline
from framework.server import PipelineServer, ServerConfig
from framework.server.app_factory import AppFactory
from framework.store.store_factory import StoreFactory
from .demo_util import TestConfig, DummyConfig

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
        server.register_module(DummyConfig, StorageInterceptor)
        store = StoreFactory.create_store()

        dummy_config = DummyConfig()
        dummy_config.dummy = 'random value'

        dummy_pipeline = DummyPipeline()
        dummy_pipeline.config = [dummy_config.create_memento()]
        pipeline_memento = dummy_pipeline.create_memento()

        store.save_pipeline('dummy_pipeline', pipeline_memento)
        restored_pipeline_memento = store.restore_pipeline('dummy_pipeline')

        assert pipeline_memento.config[0].config == restored_pipeline_memento.config[0].config

        restored_pipeline = DummyPipeline()
        restored_pipeline.set_memento(restored_pipeline_memento)
        assert dummy_pipeline.config[0].config == restored_pipeline.config[0].config

        store.delete_pipeline('dummy_pipeline')
"""
