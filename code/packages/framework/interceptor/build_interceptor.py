from abc import abstractmethod

from . import ConfigurableInterceptor
from ..context import BuildContext


class BuildInterceptor(ConfigurableInterceptor):

    @abstractmethod
    def on_build(self, context: BuildContext) -> None:
        ...
