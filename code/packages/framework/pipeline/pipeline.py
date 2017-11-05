from types import List

from ..context import SourceContext
from ..dispatcher import SourceDispatcher
from ..pipeline import PipelineBase
from ..config import ConfigModel

# Define our own type annotations
Configs = List[ConfigModelBase]

class Pipeline(PipelineBase):
    def __init__(self) -> None:
        self._source_dispatcher: SourceDispatcher = SourceDispatcher()
        self._configs: Configs = None

    @property
    def source_dispatcher(self) -> SourceDispatcher:
        return self._source_dispatcher

    def execute(self) -> None:
        self._source_dispatcher.dispatch(SourceContext(self))

    def create_memento(self) -> str:
        # Create an array of Strings
        return [c.__name__ for c in self._configs]

    def restore_from_memento(self, memento: str) -> None:
        # Convert from String array to array of Classes
        self._configs = [sys.modules[c] for c in memento]
