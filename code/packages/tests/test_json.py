import unittest

from framework.json import JsonRequest, JsonSanitizer, JsonKeyStripper


class Tests(unittest.TestCase):

    def sanitize_test(self):
        sanitized = '[{\'a\': 1, \'b\': 2, \'c\': 3, \'d\': [{\'da\': 4}], \'e\': {\'ea\': 5}}]'
        unsanitized = '[{"a":1,"b":2,"c":3,"d":[{"da":4}],"e": {"ea":5}}]'
        json_request = JsonRequest(unsanitized)
        json_request.accept(JsonSanitizer())
        self.assertTrue(sanitized == json_request.text)
