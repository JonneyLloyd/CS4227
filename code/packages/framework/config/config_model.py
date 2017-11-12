from abc import ABC, abstractmethod
from typing import Any, Type, Dict
from inflection import underscore

from .config_model_base import ConfigModelBase
from ..config import ConfigMemento, attribute_property, ConfigModelToMap, ConfigModelFromMap, ConfigModelToSchema


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
        if not hasattr(cls, '__documentname__'):
            cls.__documentname__ = underscore(cls.__name__)

    def set_memento(self, memento: ConfigMemento) -> None:
        config = memento.config
        ConfigModelFromMap().convert(config[self.__documentname__], self)

    def create_memento(self) -> ConfigMemento:
        name = self.__documentname__
        config = {name: ConfigModelToMap().convert(self), 'concrete_key': name}
        memento = ConfigMemento()
        memento.config = config
        return memento

    @classmethod
    def create_schema(cls) -> Dict:
        return ConfigModelToSchema().convert(cls)
