import logging
import spur

from framework.interceptor import DeployInterceptor
from framework.context import DeployContext
from . import RemoteDeployConfig


class RemoteDeployInterceptor(DeployInterceptor[RemoteDeployConfig]):
    def __init__(self):
        ...

    def pre_deploy(self, context: DeployContext) -> None:
        ...

    def on_deploy(self, context: DeployContext) -> None:
        ...

    def post_deploy(self, context: DeployContext) -> None:
        ...
