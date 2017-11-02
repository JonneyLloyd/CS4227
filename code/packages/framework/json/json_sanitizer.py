from framework.json import JsonVisitor, JsonRequest
from framework.util.overload import overload
import json


class JsonSanitizer(JsonVisitor):

    @overload
    def visit(self, json_request: JsonRequest) -> str:
        return str(json.loads(json_request.text))

