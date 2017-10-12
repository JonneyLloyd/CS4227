from ..context import SourceContext
from ..dispatcher import SourceDispatcher
from ..pipeline import PipelineBase


class Pipeline(PipelineBase):

    def __init__(self) -> None:
        self._source_dispatcher: SourceDispatcher = SourceDispatcher()

    @property
    def source_dispatcher(self) -> SourceDispatcher:
        return self._source_dispatcher

    def execute(self) -> None:
        self._source_dispatcher.dispatch(SourceContext(self))
