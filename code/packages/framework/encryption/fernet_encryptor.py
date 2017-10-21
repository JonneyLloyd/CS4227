from framework.encryption import Encryptor
from cryptography.fernet import Fernet


class FernetEncryptor(Encryptor):

    def __init__(self) -> None:
        self._key = Fernet.generate_key()
        self._suite = Fernet(self._key)

    def encrypt(self, text: str) -> bytes:
        return self._suite.encrypt(text.encode())

    def decrypt(self, _bytes: bytes) -> str:
        return self._suite.decrypt(_bytes).decode()
