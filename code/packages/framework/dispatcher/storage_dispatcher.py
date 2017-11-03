from typing import List

from ..context import StorageContext
from ..interceptor import StorageInterceptor


class SourceDispatcher():

    def __init__(self) -> None:
        self._interceptors: List[StorageInterceptor] = []

    def dispatch(self, context: StorageContext) -> None:
        for interceptor in self._interceptors:
            interceptor.on_source(context)

    def register(self, interceptor: StorageInterceptor) -> None:
        self._interceptors.append(interceptor)

    def remove(self, interceptor: StorageInterceptor) -> None:
        self._interceptors.remove(interceptor)
