from unittest import TestCase
from os import environ

from framework.context import SourceContext
from framework.interceptor import SourceInterceptor
from framework.config import ConfigModel, attribute_property
from framework.pipeline import Pipeline, PipelineManager
from framework.server import PipelineServer, ServerConfig
from framework.server.app_factory import AppFactory
from framework.store.store_factory import StoreFactory


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


class DummyPipeline(Pipeline):
    ...


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


class DemoInterceptor(SourceInterceptor[DummyConfig]):
    """
    Dummy class for demonstratating arbitrary features of the framework.
    """

    def pre_source(self, context: SourceContext) -> None:
        print(f"The DemoInterceptor received an event! Config a='{self.config.a}'")

    def on_source(self, context: SourceContext) -> None:
        print(f"The DemoInterceptor received an event! Config a='{self.config.a}'")


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

    def test_pipeline_save_restore(self):
        server = PipelineServer(TestConfig())
        server.register_module(DummyConfig, DemoInterceptor)

        dummy_config = DummyConfig()
        dummy_config.dummy = 'random value'
        demo_interceptor = DemoInterceptor()
        demo_interceptor.config = dummy_config

        pipeline_manager = PipelineManager()
        dummy_pipeline = pipeline_manager.create_pipeline('dummy_pipeline')
        dummy_pipeline.config = [demo_interceptor]

        pipeline_manager.save_pipeline_to_database('dummy_pipeline', dummy_pipeline)

        restored_pipeline = pipeline_manager.restore_pipeline_from_database('dummy_pipeline')

        assert dummy_pipeline.config[0].config.__dict__ == restored_pipeline.config[0].config.__dict__
        assert dummy_pipeline.config[0].config == restored_pipeline.config[0].config
        assert dummy_pipeline.config[0] == restored_pipeline.config[0]
        assert dummy_pipeline == restored_pipeline

        pipeline_manager.delete_pipeline_from_database('dummy_pipeline')

