from abc import ABC, abstractmethod


class Encryptor(ABC):

    @abstractmethod
    def encrypt(self, text: str) -> bytes:
        ...

    @abstractmethod
    def decrypt(self, _bytes: bytes) -> str:
        ...
