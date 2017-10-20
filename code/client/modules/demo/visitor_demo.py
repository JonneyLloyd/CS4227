from framework.visitor.json_key_sanitizer import JsonKeySanitizer
from framework.visitor.json_request import JsonRequest

text = '[{"a ":1, " b":2, "  c  ":3, "   d   ": [{"  da  ": 4}], " e ": {" ea ": 5}}]'
json_request = JsonRequest(text)

print(json_request.json)
visitables = [JsonKeySanitizer()]
for visitable in visitables:
    visitable.accept(json_request)
print(json_request.json)
