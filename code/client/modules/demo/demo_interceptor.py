from framework.interceptor import SourceInterceptor
from framework.context import SourceContext
from framework.config import ConfigMemento

from ..demo import DemoConfig


class DemoInterceptor(SourceInterceptor[DemoConfig]):
    """
    Dummy class for demonstratating arbitrary features of the framework.
    """

    def on_source(self, context: SourceContext) -> None:
        print(f"The DemoInterceptor received an event! Config a='{self.config.a}'")
