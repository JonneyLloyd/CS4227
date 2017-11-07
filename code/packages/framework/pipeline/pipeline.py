from types import List

from ..context import SourceContext
from ..dispatcher import SourceDispatcher
from ..pipeline import PipelineBase
from ..config import ConfigMemento

# Define our own type annotations
ConfigMementoList = List[ConfigMemento]

class Pipeline(PipelineBase):
    def __init__(self) -> None:
        self._source_dispatcher: SourceDispatcher = SourceDispatcher()
        self._configs: Configs = None

    def _create_config(self, memento: ConfigMemento):
        config = ConfigModel()
        config.set_memento(memento)
        return config

    @property
    def source_dispatcher(self) -> SourceDispatcher:
        return self._source_dispatcher

    def execute(self) -> None:
        self._source_dispatcher.dispatch(SourceContext(self))

    def create_memento(self) -> ConfigMementoList:
        # Create an array of Strings
        return [c.create_memento() for c in self._configs]

    def restore_from_memento(self, mementos: ConfigMementoList) -> None:
        # Recreate the pipeline using a list of Config Mementos
        self._configs = [self._create_config(memento) for memento in mementos]
        # TODO: Create the list of interceptor(s)
        # Register with the Dispatcher
        # for interceptor in interceptors:
        #   self._source_dispatcher.register(interceptor)
