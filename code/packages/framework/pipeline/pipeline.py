from framework.context import SourceContext
from framework.dispatcher import SourceDispatcher
from framework.pipeline import PipelineBase
from framework.pipeline.pipline_memento import PipelineMemento


class Pipeline(PipelineBase):

    def __init__(self) -> None:
        self._source_dispatcher: SourceDispatcher = SourceDispatcher()

    @property
    def source_dispatcher(self) -> SourceDispatcher:
        return self._source_dispatcher

    def execute(self) -> None:
        self._source_dispatcher.dispatch(SourceContext(self))

    def set_memento(self, memento: PipelineMemento) -> None:
        self.config = memento.config

    def create_memento(self) -> PipelineMemento:
        memento = PipelineMemento()
        memento.config = self.config
        return memento
