from typing import Type, TypeVar, Generic

from ..util import GenericABC, overload
from ..config import ConfigModel, ConfigMemento
T = TypeVar('T', bound=ConfigModel)


class ConfigurableInterceptor(GenericABC, Generic[T]):
    """
    A generic base class responsible for creating the appropriate ConfigModel for interceptors.
    """

    @property
    def config(self) -> ConfigModel:
        return self._config

    @config.setter
    @overload
    def config(self, config: ConfigMemento) -> None:
        self._config = self._create_config(config)

    @config.setter
    @overload
    def config(self, config: ConfigModel) -> None:
        assert isinstance(config, self._get_generic_type(T))
        self._config = config

    def _create_config(self, config: ConfigMemento) -> T:
        clazz: Type = self._get_generic_type(T)
        c: T = clazz()
        c.set_memento(config)
        return c
