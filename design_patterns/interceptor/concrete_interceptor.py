from .interceptor import Interceptor
from .context_object import ContextObject


class ConcreteInterceptor(Interceptor):

    def event_callback(self, context: ContextObject) -> None:
        print("ContextObject intercepted")
        context.consume_service()
