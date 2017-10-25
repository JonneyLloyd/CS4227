from framework.json import Visitor, JsonRequest
from typing import Union
import json


class JsonKeyStripper(Visitor):

    def visit(self, json_request: JsonRequest) -> str:
        return self.strip_keys(json_request.text)

    def strip_keys(self, text: str) -> str:
        _json = json.loads(text)
        self.__iterate_json(_json)
        return json.dumps(_json)

    def __iterate_json(self, _json: Union[dict, list]):
        if isinstance(_json, dict):
            self.__strip_dict_keys(_json)
        elif isinstance(_json, list):
            for element in _json:
                self.__iterate_json(element)

    def __strip_dict_keys(self, _json: dict):
        for key in _json:
            if isinstance(_json[key], dict) or isinstance(_json[key], list):
                self.__iterate_json(_json[key])
            stripped_key = key.strip()
            if key != stripped_key:
                _json[stripped_key] = _json[key]
                del _json[key]
