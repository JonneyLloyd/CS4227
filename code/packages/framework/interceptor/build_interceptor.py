from abc import abstractmethod
from typing import TypeVar, Generic

from . import ConfigurableInterceptor
from ..context import BuildContext
from ..config import ConfigModel
T = TypeVar('T', bound=ConfigModel)


class BuildInterceptor(ConfigurableInterceptor[T], Generic[T]):

    @abstractmethod
    def pre_build(self, context:BuildContext) -> None:
        ...

    @abstractmethod
    def on_build(self, context: BuildContext) -> None:
        ...