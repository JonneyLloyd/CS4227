from abc import abstractmethod
from typing import TypeVar, Generic

from . import ConfigurableInterceptor
from ..context import SourceContext
from ..config import ConfigModel
T = TypeVar('T', bound=ConfigModel)


class SourceInterceptor(ConfigurableInterceptor[T], Generic[T]):

    @abstractmethod
    def pre_source(selfs, context: SourceContext) -> None:
        ...

    @abstractmethod
    def on_source(self, context: SourceContext) -> None:
        ...
