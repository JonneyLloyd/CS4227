from typing import List

from flask import Flask
from framework.server import PipelineServer

from .document_store import DocumentStore


class DynamoStore(DocumentStore):

    def __init__(self, server: PipelineServer):
        self._app = server.app

    def save(self, name: str, _list: List[dict]) -> None:
        table = self._app.extensions['dynamo'].tables['mementos']
        table.put_item(Item={
            'type': name,
            'config': _list
        })

    def restore(self, name: str) -> List[dict]:
        table = self._app.extensions['dynamo'].tables['mementos']
        return table.get_item(Key={'type': name})['Item']['config']

    def delete(self, name: str) -> None:
        table = self._app.extensions['dynamo'].tables['mementos']
        table.delete_item(Key={'type': name})