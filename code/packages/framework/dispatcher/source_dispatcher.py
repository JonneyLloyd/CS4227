from typing import List

from ..context import SourceContext
from ..interceptor import SourceInterceptor


class SourceDispatcher():

    def __init__(self) -> None:
        self._interceptors: List[SourceInterceptor] = []

    def dispatch(self, context: SourceContext) -> None:
        for interceptor in self._interceptors:
            interceptor.on_source(context)

    def register(self, interceptor: SourceInterceptor) -> None:
        self._interceptors.append(interceptor)

    def remove(self, interceptor: SourceInterceptor) -> None:
        self._interceptors.remove(interceptor)
