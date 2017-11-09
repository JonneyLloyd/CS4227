from typing import List

from ..context import BuildContext
from ..interceptor import BuildInterceptor


class BuildDispatcher():

    def __init__(self) -> None:
        self._interceptors: List[BuildInterceptor] = []

    def dispatch(self, context: BuildContext) -> None:
        for interceptor in self._interceptors:
            interceptor.on_build(context)

    def register(self, interceptor: BuildInterceptor) -> None:
        self._interceptors.append(interceptor)

    def remove(self, interceptor: BuildInterceptor) -> None:
        self._interceptors.remove(interceptor)
