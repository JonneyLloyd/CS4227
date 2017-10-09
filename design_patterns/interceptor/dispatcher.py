from .interceptor import Interceptor
from .context_object import ContextObject


class Dispatcher():

    def __init__(self):
        self.interceptor_list = []

    def callback(self, context: ContextObject) -> None:
        print("callback()")
        self.context = context
        self.iterate_list()

    def dispatch(self, interceptor: Interceptor) -> None:
        interceptor.event_callback(self.context)

    def register(self, interceptor: Interceptor) -> None:
        self.interceptor_list.append(interceptor)

    def remove(self, interceptor: Interceptor) -> None:
        self.interceptor_list.remove(interceptor)

    def iterate_list(self) -> None:
        for x in self.interceptor_list:
            self.dispatch(x)
