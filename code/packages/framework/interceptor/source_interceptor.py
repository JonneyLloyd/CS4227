from abc import abstractmethod
from typing import TypeVar, Generic

from ..interceptor import ConfigurableInterceptor
from ..context import SourceContext
from ..config import ConfigModel


T = TypeVar('T', bound=ConfigModel)
class SourceInterceptor(ConfigurableInterceptor[T], Generic[T]):

    @abstractmethod
    def on_source(self, context: SourceContext) -> None:
        ...
