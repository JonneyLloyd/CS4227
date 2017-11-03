from typing import List

from ..context import DeployContext
from ..interceptor import DeployInterceptor


class SourceDispatcher():

    def __init__(self) -> None:
        self._interceptors: List[DeployInterceptor] = []

    def dispatch(self, context: DeployContext) -> None:
        for interceptor in self._interceptors:
            interceptor.on_source(context)

    def register(self, interceptor: DeployInterceptor) -> None:
        self._interceptors.append(interceptor)

    def remove(self, interceptor: DeployInterceptor) -> None:
        self._interceptors.remove(interceptor)
