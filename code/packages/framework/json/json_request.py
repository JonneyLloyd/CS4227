from framework.json import Visitable, Visitor


class JsonRequest(Visitable):

    def __init__(self, text: str) -> None:
        self._text = text

    def accept(self, visitor: Visitor) -> None:
        self._text = visitor.visit(self)

    @property
    def text(self) -> str:
        return self._text
