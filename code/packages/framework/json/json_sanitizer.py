from framework.json import Visitor, JsonRequest
import json


class JsonSanitizer(Visitor):

    def visit(self, json_request: JsonRequest) -> str:
        return str(json.loads(json_request.text))

