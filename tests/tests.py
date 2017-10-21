import unittest


class Tests(unittest.TestCase):

    def encrypt_test(self):
        text = "Hello World!"
        from framework.encryption import Encryption, FernetEncryptor
        encryption = Encryption(FernetEncryptor())
        encrypted = encryption.encrypt(text)
        self.assertTrue(text != encrypted)
        self.assertTrue(isinstance(encrypted, bytes) and text != encrypted)

    def decrypt_test(self):
        text = "Hello World!"
        from framework.encryption import Encryption, FernetEncryptor
        encryption = Encryption(FernetEncryptor())
        encrypted = encryption.encrypt(text)
        self.assertTrue(text == encryption.decrypt(encrypted))

    def sanitize_test(self):
        sanitized = '[{\'a\': 1, \'b\': 2, \'c\': 3, \'d\': [{\'da\': 4}], \'e\': {\'ea\': 5}}]'
        unsanitized = '[{"a":1,"b":2,"c":3,"d":[{"da":4}],"e": {"ea":5}}]'
        from framework.json import JsonRequest, JsonSanitizer
        json_request = JsonRequest(unsanitized)
        json_request.accept(JsonSanitizer())
        self.assertTrue(sanitized == json_request.text)

    def key_strip_test(self):
        stripped = '[{"a": 1, "b": 2, "c": 3, "d": [{"da": 4}], "e": {"ea": 5}}]'
        unstripped = '[{" a ":1,"   b   ":2,"   c   ":3,"  d ":[{"   da  ":4}],"  e  ": {"  ea  ":5}}]'
        from framework.json import JsonRequest, JsonKeyStripper
        json_request = JsonRequest(unstripped)
        json_request.accept(JsonKeyStripper())
        self.assertTrue(stripped == json_request.text)


if __name__ == '__main__':
    unittest.main()