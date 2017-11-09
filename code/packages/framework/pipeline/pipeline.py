from typing import List

from framework.context import SourceContext
from framework.dispatcher import SourceDispatcher
from framework.pipeline import PipelineBase
from framework.pipeline.pipeline_memento import PipelineMemento
from framework.config import ConfigMemento, ConfigModel

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

    def set_memento(self, memento: PipelineMemento) -> None:
        self.config = [self._create_config(config_memento) for config_memento in memento.config]

    def create_memento(self) -> PipelineMemento:
        memento = PipelineMemento()
        configs = [config.create_memento() for config in self.config]
        memento.config = configs
        return memento
