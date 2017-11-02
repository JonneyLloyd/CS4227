from framework.json import Visitable


class JsonRequest(Visitable):

    def __init__(self, text: str) -> None:
        self._text = text

    def accept(self, visitor: 'JsonVisitor') -> None:
        self._text = visitor.visit(self)

    @property
    def text(self) -> str:
        return self._text
