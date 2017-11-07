from framework.pipeline import PipelineBase
from framework.pipeline.pipline_memento import PipelineMemento
from ..context import SourceContext, BuildContext, PackageContext, DeployContext
from ..dispatcher import SourceDispatcher, BuildDispatcher, PackageDispatcher, DeployDispatcher
from ..pipeline import PipelineBase


class Pipeline(PipelineBase):

    def __init__(self) -> None:
        self._source_dispatcher: SourceDispatcher = SourceDispatcher()
        self._build_dispatcher: BuildDispatcher = BuildDispatcher()
        self._package_dispatcher: PackageDispatcher = PackageDispatcher()
        self._deploy_dispatcher: DeployDispatcher = DeployDispatcher()

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

    def execute(self) -> None:
        self._source_dispatcher.dispatch(SourceContext(self))
        self._build_dispatcher.dispatch(BuildContext(self))
        self._package_dispatcher.dispatch(PackageContext(self))
        self._deploy_dispatcher.dispatch(DeployContext(self))

    def set_memento(self, memento: PipelineMemento) -> None:
        self.config = memento.config

    def create_memento(self) -> PipelineMemento:
        memento = PipelineMemento()
        memento.config = self.config
        return memento

