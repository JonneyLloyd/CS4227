from pickle import dumps
from types import List

from ..context import SourceContext
from ..dispatcher import SourceDispatcher
from ..pipeline import PipelineBase
from ..config import ConfigModel

# Define our own type annotations
Configs = List[ConfigModelBase]

class Pipeline(PipelineBase):
    def __init__(self, configs: Configs) -> None:
        self._source_dispatcher: SourceDispatcher = SourceDispatcher()
        self._configs: Configs = configs

    @property
    def source_dispatcher(self) -> SourceDispatcher:
        return self._source_dispatcher

    def execute(self) -> None:
        self._source_dispatcher.dispatch(SourceContext(self))

    def create_memento(self) -> str:
        '''Returns a pickle object represented as a string'''
        return dumps(vars(self))

    def restore_from_memento(self, memento: str) -> None:
        '''Converts the str back to a pickle object
        and updates our current object'''
        state = pickle.loads(memento)
        vars(self).clear()
        vars(self).update(state)
