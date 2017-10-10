from abc import ABCMeta, abstractmethod


class Context(object, metaclass=ABCMeta):
    @abstractmethod
    def run(self) -> None:
        pass

class State(object, metaclass=ABCMeta):
    def __init__(self, context):
        self._context = context
        print(f'Set state: {type(self).__name__}')

    @abstractmethod
    def run(self) -> None:
        pass


class ConcreteStateA(State):
    def run(self) -> None:
        self._context.set_state(ConcreteStateB(self._context))


class ConcreteStateB(State):
    def run(self) -> None:
        self._context.set_state(ConcreteStateA(self._context))


class ConcreteContext(Context):
    def __init__(self):
        self._state = ConcreteStateA(self)

    def run(self) -> None:
        self._state.run()

    def set_state(self, state) -> None:
        self._state = state
