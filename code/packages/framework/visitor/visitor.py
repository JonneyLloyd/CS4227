from abc import ABC, abstractmethod
# TODO not sure why i can't import this... python... hmmm....
# from framework.visitor.json_key_sanitizer import JsonKeySanitizer


class Visitor(ABC):

    @abstractmethod
    def visit(self, json_key_sanitizer: 'JsonKeySanitizer') -> None:
        raise NotImplementedError()
