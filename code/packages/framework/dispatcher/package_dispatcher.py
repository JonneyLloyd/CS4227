from typing import List

from ..context import PackageContext
from ..interceptor import PackageInterceptor


class SourceDispatcher():

    def __init__(self) -> None:
        self._interceptors: List[PackageInterceptor] = []

    def dispatch(self, context: PackageContext) -> None:
        for interceptor in self._interceptors:
            interceptor.on_source(context)

    def register(self, interceptor: PackageInterceptor) -> None:
        self._interceptors.append(interceptor)

    def remove(self, interceptor: PackageInterceptor) -> None:
        self._interceptors.remove(interceptor)
