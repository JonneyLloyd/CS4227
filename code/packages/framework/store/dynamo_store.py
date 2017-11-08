from typing import List

from framework.server import dynamo
from .document_store import DocumentStore


class DynamoStore(DocumentStore):

    def __init__(self):
        self.store = dynamo

    def _save(self, name: str, _list: List[dict]) -> None:
        table = self.store.tables['mementos']
        table.put_item(Item={
            'type': name,
            'config': _list
        })

    def _restore(self, name: str) -> List[dict]:
        table = self.store.tables['mementos']
        return table.get_item(Key={'type': name})['Item']['config']

    def _delete(self, name: str) -> None:
        table = self.store.tables['mementos']
        table.delete_item(Key={'type': name})
