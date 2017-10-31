from framework.json import Visitor, JsonRequest
from framework.util.overload import overload
import json


class JsonSanitizer(Visitor):

    @overload
    def visit(self, json_request: JsonRequest) -> str:
        return str(json.loads(json_request.text))

