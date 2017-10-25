import unittest

from framework.encryption import Encryption, FernetEncryptor


class Tests(unittest.TestCase):

    def encrypt_test(self):
        text = "Hello World!"
        encryption = Encryption(FernetEncryptor())
        encrypted = encryption.encrypt(text)
        self.assertTrue(text != encrypted)
        self.assertTrue(isinstance(encrypted, bytes) and text != encrypted)

    def decrypt_test(self):
        text = "Hello World!"
        encryption = Encryption(FernetEncryptor())
        encrypted = encryption.encrypt(text)
        self.assertTrue(text == encryption.decrypt(encrypted))
