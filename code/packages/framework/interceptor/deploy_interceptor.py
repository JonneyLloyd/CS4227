from abc import abstractmethod
from typing import TypeVar, Generic

from . import ConfigurableInterceptor
from ..context import DeployContext
from ..config import ConfigModel
T = TypeVar('T', bound=ConfigModel)


class DeployInterceptor(ConfigurableInterceptor[T], Generic[T]):

    @abstractmethod
    def pre_deploy(self, context: DeployContext) -> None:
        ...

    @abstractmethod
    def on_deploy(self, context: DeployContext) -> None:
        ...
