from framework.store.document_store import DocumentStore

from .dynamo_store import DynamoStore


class StoreFactory:

    @staticmethod
    def create_store() -> DocumentStore:
        return DynamoStore()
