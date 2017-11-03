from abc import abstractmethod
from typing import TypeVar, Generic

from . import ConfigurableInterceptor
from ..context import StorageContext
from ..config import ConfigModel


T = TypeVar('T', bound=ConfigModel)
class StorageInterceptor(ConfigurableInterceptor[T], Generic[T]):

    @abstractmethod
    def on_storage(self, context: StorageContext) -> None:
        ...
