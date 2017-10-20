from framework.visitor.visitable import Visitable
from framework.visitor.visitor import Visitor
from typing import Union


class JsonKeySanitizer(Visitable):

    def accept(self, visitor: Visitor) -> None:
        visitor.visit(self)

    def sanitize(self, json: Union[dict, list]) -> None:
        if isinstance(json, dict):
            self.__strip_dict_keys(json)
        elif isinstance(json, list):
            for element in json:
                self.sanitize(element)

    def __strip_dict_keys(self, json: dict) -> None:
        for key in json:
            if isinstance(json[key], dict) or isinstance(json[key], list):
                self.sanitize(json[key])
            stripped_key = key.strip()
            if key != stripped_key:
                json[stripped_key] = json[key]
                del json[key]
