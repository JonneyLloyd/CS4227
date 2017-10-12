import pickle

class Originator:
    def __init__(self):
        self._state = ''

    def set(self, state: str) -> None:
        print(f'Setting State: {state}')
        self._state = state
        self.print_state()

    def create_memento(self) -> str:
        print('Saving State')
        return pickle.dumps(vars(self))

    def print_state(self) -> None:
        print(f'Current State: {self._state}')

    def restore_from_memento(self, memento: str) -> None:
        print('Restoring State')
        state = pickle.loads(memento)
        vars(self).clear()
        vars(self).update(state)
        self.print_state()
