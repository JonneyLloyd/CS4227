from .interceptor import Interceptor
from .context_object import ContextObject


class Dispatcher():

    def __init__(self):
        self.interceptor_list = []

    def callback(self, context: ContextObject) -> None:
        print("callback()")
        for x in self.interceptor_list:
            x.event_callback(context)

    def register(self, interceptor: Interceptor) -> None:
        self.interceptor_list.append(interceptor)

    def remove(self, interceptor: Interceptor) -> None:
        self.interceptor_list.remove(interceptor)
