from abc import ABC, abstractmethod

from ..config import ConfigMemento


class ConfigurableInterceptor(ABC):

    @property  # type: ignore  # https://github.com/python/mypy/issues/1362
    @abstractmethod
    def config(self) -> ConfigMemento:
        ...

    @config.setter  # type: ignore
    @abstractmethod
    def config(self, config: ConfigMemento) -> None:
        ...
