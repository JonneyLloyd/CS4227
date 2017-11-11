from typing import Type, Any, Optional, Sequence, Mapping, Dict, Callable
from inflection import underscore

from ..util import overload
from .config_model_base import ConfigModelBase
from ..config import attribute_property


class ConfigModelToMap:

    def convert(self, item: ConfigModelBase) -> Mapping[str, Any]:
        """
        Loads the values from a ConfigModel to a new map.

        Facilitates the creation of a memento.
        """
        return self._to_dict(item)

    @overload
    def _to_dict(self, item: ConfigModelBase) -> Any:
        model: Dict[str, attribute_property] = item.subclasses_attribute_properties[item.__class__]
        model_map = {}
        for k, attr_prop in model.items():
            v = self._to_dict(getattr(item, k))
            if attr_prop.attribute.required and v is None:
                raise ValueError(f"'{k}' is None but is a required value, expected non-None value.")
            model_map[attr_prop.attribute.name] = v
        return model_map

    @overload
    def _to_dict(self, item: Sequence) -> Any:
        return [self._to_dict(i) for i in item]

    @overload
    def _to_dict(self, item: Mapping) -> Any:
        return {k: self._to_dict(v) for k, v in item.items()}

    @overload
    def _to_dict(self, item: str) -> Any:
        return item

    @overload
    def _to_dict(self, item: int) -> Any:
        return item

    @overload
    def _to_dict(self, item: float) -> Any:
        return item

    @overload
    def _to_dict(self, item: bool) -> Any:
        return item

    @overload
    def _to_dict(self, item: type(None)) -> Any:
        return None


class ConfigModelFromMap:

    def convert(self, item: Mapping[str, Any], target: ConfigModelBase) -> None:
        """
        Loads the values from a map into a ConfigModel.

        Facilitates the restoration of a memento.
        """
        return self._to_config(item, target)

    @overload
    def _to_config(self, item: Mapping, target: ConfigModelBase) -> None:
        model: Dict[str, attribute_property] = target.subclasses_attribute_properties[target.__class__]
        for attr_prop in model.values():
            key = attr_prop.attribute.name
            type_info = attr_prop.attribute.type_info
            v = None
            if key in item:
                item_value = item.get(key)
                if issubclass(type_info, tuple([str, int, float, bool, type(None)])):
                    v = item_value
                elif issubclass(type_info, ConfigModelBase):
                    v = type_info()
                    self._to_config(item_value, v)
                elif issubclass(type_info, Mapping):
                    if issubclass(type_info.__parameters__[1], ConfigModelBase):
                        v = {}
                        for k, v in item_value.items():
                            instance = type_info.__parameters__[1]()
                            self._to_config(v, instance)
                            v[k] = instance
                    else:
                        v = {k: v for k, v in item_value.items()}
                elif issubclass(type_info, Sequence):
                    if issubclass(type_info.__args__[0], ConfigModelBase):
                        v = []
                        for t in item_value:
                            instance = type_info.__args__[0]()
                            self._to_config(t, instance)
                            v.append(instance)
                    else:
                        v = [t for t in item_value]

            if attr_prop.attribute.required and v is None:
                raise ValueError(f"'{key}' is None but is a required value, expected non-None value.")
            attr_prop.__set__(target, v)


class ConfigModelToSchema:

    def convert(self, item: ConfigModelBase) -> Mapping[str, Any]:
        """
        Create a schema for a ConfigModel.

        Facilitates the API.
        """
        return self._to_schema(item)

    @overload
    def _to_schema(self, target: Type) -> Mapping[str, Any]:
        model: Dict[str, attribute_property] = target.subclasses_attribute_properties[target]
        model_map = {}
        required = []
        definitions = {}

        for attr_prop in model.values():
            key = attr_prop.attribute.name
            type_info = attr_prop.attribute.type_info

            type_str, type_ref, defin = self._to_schema_element(key, type_info)

            model_map[key] = {'type': type_str}

            if type_ref:
                model_map[key]['ref'] = type_ref

            definitions.update(defin)

            if attr_prop.attribute.required:
                required.append(key)

        schema = {'documentname': target.__documentname__,
                  'type': 'object',
                  'properties': model_map}

        if required:
            schema['required'] = required
        if definitions:
            schema['definitions'] = definitions

        return schema

    def _to_schema_element(self, key: str, type_info: Type) -> Any:
        type_str = None
        type_ref = None
        definitions = {}

        if issubclass(type_info, tuple([str, int, float, bool])):
            type_str = self._to_type_str(type_info)

        elif issubclass(type_info, ConfigModelBase):
            type_str = 'object'
            type_ref = f'definitions/{type_info.__documentname__}'
            definitions[type_info.__documentname__] = self._to_schema(type_info)

        elif issubclass(type_info, Mapping):
            if issubclass(type_info.__parameters__[1], ConfigModelBase):
                type_param_value = type_info.__parameters__[1].__documentname__
            else:
                type_param_value = self._to_type_str(type_info.__parameters__[1])
            type_str = 'object'
            type_param_key = self._to_type_str(type_info.__parameters__[0])
            type_ref = f'definitions/map[{type_param_key},{type_param_value}]'
            definitions[f'map[{type_param_key},{type_param_value}]'] = {'type': 'map', 'type_params': [type_param_key, type_param_value]}

        elif issubclass(type_info, Sequence):
            if issubclass(type_info.__args__[0], ConfigModelBase):
                type_param = type_info.__args__[0].__documentname__
            else:
                type_param = self._to_type_str(type_info.__args__[0])
            type_str = 'object'
            type_ref = f'definitions/list[{type_param}]'
            definitions[f'list[{type_param}]'] = {'type': 'list', 'type_params': [type_param]}

        return type_str, type_ref, definitions

    def _to_type_str(self, typ: Type) -> str:
        if issubclass(typ, str):
            return 'string'
        elif issubclass(typ, int):
            return 'integer'
        elif issubclass(typ, float):
            return 'float'
        elif issubclass(typ, bool):
            return 'boolean'
