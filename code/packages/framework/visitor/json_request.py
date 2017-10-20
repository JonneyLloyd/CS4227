from framework.visitor.json_key_sanitizer import JsonKeySanitizer
from framework.visitor.visitor import Visitor
from typing import Union
import json


class JsonRequest(Visitor):

    def __init__(self, json_str: str) -> None:
        self._json = json.loads(json_str)
        self._valid = True

    def visit(self, json_key_sanitizer: JsonKeySanitizer) -> None:
        print(self.__class__ , "is visiting", json_key_sanitizer.__class__)
        json_key_sanitizer.sanitize(self._json)

    @property
    def json(self) -> Union[dict, list]:
        return self._json

    @property
    def valid(self) -> bool:
        return self._valid
