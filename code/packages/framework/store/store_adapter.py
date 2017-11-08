from framework.pipeline import PipelineBase
from framework.pipeline.pipline_memento import PipelineMemento
from framework.store.store_adaptee import StoreAdaptee
from .document_store import DocumentStore


class StoreAdapter(StoreAdaptee):

    def __init__(self, store: DocumentStore) -> None:
        super().__init__(store)

    def save(self, memento: PipelineMemento) -> None:
        self.save_pipeline(memento)

    def restore(self, name: str) -> PipelineMemento:
        return self.restore_pipeline(name)

    def delete(self, name: str) -> None:
        self.store.delete(name)
