from abc import abstractmethod

from . import ConfigurableInterceptor
from ..context import SourceContext


class SourceInterceptor(ConfigurableInterceptor):

    @abstractmethod
    def on_source(self, context: SourceContext) -> None:
        ...
