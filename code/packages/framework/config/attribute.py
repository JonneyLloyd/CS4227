from abc import ABC, abstractmethod
from typing import Optional, Any, Type, TypeVar, Union, Sequence, Mapping, Callable

from .config_model_base import ConfigModelBase


class Attribute:
    """Representation of fields/attributes in a document
       such as :class:`..ConfigModel`
    """

    _supported_types = [
        str, int, float, bool, ConfigModelBase,
        Sequence, Mapping
    ]

    def __init__(self, name: str, required: bool=True,
                 display_name: Optional[str]=None, display_tip: Optional[str]=None,
                 type_info: Optional[Type]=None) -> None:
        """Create a new :class:`.Attribute`.

        Parameters
        ----------
        name (str)
            The name of the attribute.
        required (bool, optional)
            Flag to require the presence of a non-None value.
        display_name: (str, optional)
            A pretty printed name for the attribute.
        display_tip: (str, optional)
            An explanation of what the attribute field should contain.
        type_info: (Type, optional)
            The type of the attribute. Required if type annotations are not present.

        """
        self._name = name
        self._required = required
        self._display_name = display_name
        self._display_tip = display_tip
        if type_info is not None:
            self.type_info = type_info

    @property
    def name(self) -> str:
        return self._name

    @property
    def type_info(self) -> Type:
        return self._type_info

    @type_info.setter
    def type_info(self, value: Type) -> None:
        if not any(issubclass(value, t) for t in Attribute._supported_types):
            raise TypeError(f'Attributes must be of type {Attribute._supported_types}')
        self._type_info = value

    @property
    def required(self) -> bool:
        return self._required

    @property
    def display_name(self) -> Optional[str]:
        return self._display_name

    @property
    def display_tip(self) -> Optional[str]:
        return self._display_tip

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self._name}, type_info={self._type_info}, " \
               f"required={self._required}, display_name={self._display_name}, " \
               f"display_tip={self._display_tip})"


class attribute_property:
    """A descriptor decorator which allows both instance and class level behavior
       intended for use with :class:`..Attribute` and :class:`..ConfigModel`.
    """

    def __init__(self, name: str, required: bool=True,
                 display_name: Optional[str]=None, display_tip: Optional[str]=None,
                 type_info: Optional[Type]=None) -> None:
        """Create a new :class:`.attribute_property`.

        Parameters
        ----------
        name (str)
            The name of the attribute
        required (bool, optional)
            Flag to require the presence of a non-None value
        display_name: (str, optional)
            A pretty printed name for the attribute
        display_tip: (str, optional)
            An explanation of what the attribute field should contain
        type_info: (Type, optional)
            The type of the attribute. Required if type annotations are not present.

        Usage:

            class SomeConfigClass(ConfigModel):

                @attribute_property('value', str)
                def value(self) -> str:
                    return self._value

                @value.setter
                def value(self, value: str) -> None:
                    self._value = value

            >>> var = SomeConfigClass()
            >>> var.value = 7
            >>> var.value
            7
            >>> SomeConfigClass.value
            Attribute(name=value, type_info=<class 'str'>, required=True, display_name=None, display_tip=None)

        """
        self._attribute = Attribute(name, required, display_name, display_tip, type_info)

    @property
    def attribute(self) -> Attribute:
        return self._attribute

    def __call__(self,
                 fget: Callable,
                 fset: Optional[Callable]=None,
                 fdel: Optional[Callable]=None,
                 doc: str=None) -> 'attribute_property':
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc
        if hasattr(fget, '__annotations__'):
            self._attribute.type_info = fget.__annotations__['return']
        return self

    def __get__(self, instance: Any, owner: Any):
        if instance is None:
            return self.attribute
        else:
            return self.fget(instance)

    def __set__(self, instance: Any, value: Any):
        if self.fset is None or instance is None:
            raise AttributeError("can't set attribute")
        self.fset(instance, value)

    def __delete__(self, instance: Any):
        if self.fdel is None or instance is None:
            raise AttributeError("can't delete attribute")
        self.fdel(instance)

    def setter(self, fset: Callable) -> 'self.attribute_property':
        """Decorator that defines a value-setter method."""
        self.fset = fset
        return self

    def deleter(self, fdel: Callable) -> 'self.attribute_property':
        """Decorator that defines a value-deletion method."""
        self.fdel = fdel
        return self
