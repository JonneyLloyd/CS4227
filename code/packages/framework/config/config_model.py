from abc import ABC, abstractmethod
from typing import Any, Type, Dict
from inflection import underscore

from .config_model_base import ConfigModelBase
from ..config import ConfigMemento, attribute_property, ConfigModelToMap, ConfigModelFromMap


class ConfigModel(ConfigModelBase):
    """
    Base class providing ORM like features for simple JSON-like documents.
    """

    subclasses_attribute_properties: Dict[Type, Dict[str, attribute_property]] = {}

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        attribute_properties = {name: func for name, func in vars(cls).items()
                                if isinstance(func, attribute_property)}
        cls.subclasses_attribute_properties[cls] = attribute_properties

    def __getattribute__(self, key):
        if key == '__documentname__':
            if hasattr(self.__class__, '__documentname__'):
                return self.__class__.__documentname__
            else:
                return underscore(self.__class__.__name__)
        return super().__getattribute__(key)

    def set_memento(self, memento: ConfigMemento) -> None:
        config = memento.config
        ConfigModelFromMap().convert(config[self.__documentname__], self)

    def create_memento(self) -> ConfigMemento:
        name = self.__documentname__
        config = {name: ConfigModelToMap().convert(self)}
        memento = ConfigMemento()
        memento.config = config
        return memento
