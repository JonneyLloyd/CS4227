from abc import ABC, abstractmethod
import os
class ConfigInterface(ABC):

    SECRET_KEY = os.urandom(12)
