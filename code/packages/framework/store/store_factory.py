from framework.server import PipelineServer

from .store_adapter import StoreAdapter
from .dynamo_store import DynamoStore


class StoreFactory:

    @staticmethod
    def create_store(server: PipelineServer) -> StoreAdapter:
        store = DynamoStore(server)
        return StoreAdapter(store)
