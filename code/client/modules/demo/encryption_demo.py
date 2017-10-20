from framework.encryption.encryption import Encryption
from framework.encryption.fernet_encryptor import FernetEncryptor

text = "Hello World!"
encryption = Encryption(FernetEncryptor())
encrypted = encryption.encrypt(text)
print(encrypted)
print(encryption.decrypt(encrypted))
