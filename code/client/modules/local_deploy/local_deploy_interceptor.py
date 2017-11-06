import logging
from shutil import unpack_archive

from framework.interceptor import DeployInterceptor
from framework.context import DeployContext
from . import LocalDeployConfig


class LocalDeployInterceptor(DeployInterceptor[LocalDeployConfig]):

    def __init__(self, package_path, build_root):
        self._package_path = package_path
        self._build_root = build_root

    def pre_deploy(self, context: DeployContext) -> None:
        ...

    def on_deploy(self, context: DeployContext) -> None:
        ...

    def post_deploy(self, context: DeployContext) -> None:
        ...

    def _extract_build(self) -> bool:
        unpack_archive(self._package_path, self._build_root)
