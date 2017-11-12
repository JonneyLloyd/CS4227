from typing import List
from threading import Thread

from framework.pipeline import PipelineBase
from framework.pipeline.pipeline_memento import PipelineMemento
from framework.config import ConfigMemento, ConfigModel
from framework.context import SourceContext, BuildContext, PackageContext, DeployContext
from framework.dispatcher import SourceDispatcher, BuildDispatcher, PackageDispatcher, DeployDispatcher
from framework.interceptor import SourceInterceptor, BuildInterceptor, PackageInterceptor, DeployInterceptor
from framework.control import ModuleRegistry
from framework.util import overload

# Define our own type annotations
ConfigMementoList = List[ConfigMemento]

class Pipeline(PipelineBase):
    def __init__(self) -> None:
        self._source_dispatcher: SourceDispatcher = SourceDispatcher()
        self._build_dispatcher: BuildDispatcher = BuildDispatcher()
        self._package_dispatcher: PackageDispatcher = PackageDispatcher()
        self._deploy_dispatcher: DeployDispatcher = DeployDispatcher()

    def _create_config_and_interceptor(self, memento: ConfigMemento):
        con_int_tup = ModuleRegistry.get_module(memento.config['concrete_key'])
        config = con_int_tup[0]()
        interceptor = con_int_tup[1]()
        config.set_memento(memento)
        interceptor.config = config
        self.source_dispatcher.register(interceptor)
        return interceptor

    @property
    def source_dispatcher(self) -> SourceDispatcher:
        return self._source_dispatcher

    @property
    def build_dispatcher(self) -> BuildDispatcher:
        return self._build_dispatcher

    @property
    def package_dispatcher(self) -> PackageDispatcher:
        return self._package_dispatcher

    @property
    def deploy_dispatcher(self) -> DeployDispatcher:
        return self._deploy_dispatcher

    @overload
    def register_interceptor(self, interceptor: SourceInterceptor) -> None:
        self._source_dispatcher.register(interceptor)

    @overload
    def register_interceptor(self, interceptor: BuildInterceptor) -> None:
        self._build_dispatcher.register(interceptor)

    @overload
    def register_interceptor(self, interceptor: PackageInterceptor) -> None:
        self._package_dispatcher.register(interceptor)

    @overload
    def register_interceptor(self, interceptor: DeployInterceptor) -> None:
        self._deploy_dispatcher.register(interceptor)

    def execute(self) -> None:
        self._source_dispatcher.dispatch(SourceContext(self))
        self._build_dispatcher.dispatch(BuildContext(self))
        self._package_dispatcher.dispatch(PackageContext(self))
        self._deploy_dispatcher.dispatch(DeployContext(self))

    def set_memento(self, memento: PipelineMemento) -> None:
        self.config = [self._create_config_and_interceptor(config_memento)
                        for config_memento in memento.config]

    def create_memento(self) -> PipelineMemento:
        memento = PipelineMemento()
        configs = [interceptor.config.create_memento() for interceptor in self.config]
        memento.config = configs
        return memento
