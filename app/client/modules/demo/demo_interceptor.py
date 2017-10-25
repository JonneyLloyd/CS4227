from framework.interceptor import SourceInterceptor
from framework.context import SourceContext
from framework.config import ConfigMemento


class DemoInterceptor(SourceInterceptor):

    @property
    def config(self) -> ConfigMemento:
        ...

    @config.setter
    def config(self, config: ConfigMemento) -> None:
        ...

    def on_source(self, context: SourceContext) -> None:
        print('The DemoInterceptor received an event!')
