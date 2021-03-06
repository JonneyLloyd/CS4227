from framework.encryption import Encryptor


class Encryption:

    def __init__(self, encryptor: Encryptor) -> None:
        self._encryptor = encryptor

    @property
    def encryptor(self) -> Encryptor:
        return self._encryptor

    def encrypt(self, text: str) -> bytes:
        return self._encryptor.encrypt(text)

    def decrypt(self, _bytes: bytes) -> str:
        return self._encryptor.decrypt(_bytes)