import logging
import os.path
from shutil import unpack_archive
import spur

from framework.interceptor import DeployInterceptor
from framework.context import DeployContext
from . import LocalDeployConfig


class LocalDeployInterceptor(DeployInterceptor[LocalDeployConfig]):

    def __init__(self, package_path: str, build_name: str,
                 deploy_root: str, script_list: list, packaged: bool) -> None:
        """
        Deploy an app locally - extract if packaged, run series of scripts

        Args:
            package_path: Absolute path to packaged build (path to build if not packaged)
            build_name: Name of build that is packaged (tail of packaged_path without file
                        format extension)
            deploy_root: Absolute path to root directory for deployments (If build is not
                         packaged, build will be located inside this directory by default)
            script_list: List of absolute paths of scripts to execute during deployment
                         The paths to scripts should be identical across multiple hosts
                         e.g. '/deployment/build_hello_world/app/hello_world.py'
            packaged: Boolean flag - set to true if build is packaged and set to false
                      if not packaged (flag not used for remote deploy)
        """
        self._package_path = package_path
        self._build_name = build_name
        self._deploy_root = deploy_root
        self._script_list = script_list
        self._packaged = packaged
        self._unpacked_build = self._deploy_root.rstrip('\/') + '/' + self._build_name

    def pre_deploy(self, context: DeployContext) -> None:
        pre_deploy_success = False
        if self._validate_path(self._package_path) and self._validate_path(self._deploy_root):
            if self._packaged:
                if self._copy_packaged_build() and self._extract_build():
                    logging.info('Success: pre_deploy for extracted build: ' + self._build_name)
                    pre_deploy_success = True
            elif self._validate_path(self._unpacked_build):
                logging.info('Success: pre_deploy for unpackaged build: ' + self._build_name)
                pre_deploy_success = True
        if not pre_deploy_success:
            logging.error('Failure: pre_deploy for build: ' + self._build_name)

    def on_deploy(self, context: DeployContext) -> None:
        if self._switch_local_venv():
            logging.info('Success: on_deploy for build: ' + self._build_name)
        else:
            logging.error('Failure: on_deploy for build: ' + self._build_name)

    def post_deploy(self, context: DeployContext) -> None:
        post_deploy_success = True
        for script in self._script_list:
            if self._validate_path(script):
                logging.info('Found path to script: ' + script)
            else:
                logging.error('Failed to find path to script')
                post_deploy_success = False
        if post_deploy_success and self._execute_local_scripts():
            logging.info('Success: post_deploy script execution for build: ' + self._build_name)
        else:
            logging.error('Failure: post_deploy script execution for build: ' + self._build_name)

    def _validate_path(self, path: str) -> bool:
        is_valid_path = True
        if os.path.isabs(path):
            logging.info('Located ' + path.__name__ + ": " + path)
        else:
            logging.error('Could not locate ' + path.__name__ + ": " + path)
            is_valid_path = False

        return is_valid_path

    def _copy_packaged_build(self) -> bool:
        copy_success = True
        copy_command = 'cp ' + self._package_path + " " + self._deploy_root
        copy_args = copy_command.split()

        local_shell = spur.LocalShell()
        try:
            local_shell.run(copy_args)
            logging.info('Copied packaged build for deployment: ' + copy_command)
        except spur.RunProcessError:
            logging.error('Copying packaged build for deployment failed: ' + copy_command)
            copy_success = False

        return copy_success

    def _extract_build(self) -> bool:
        extract_success = True
        if unpack_archive(self._package_path, self._deploy_root):
            logging.info('Extracted archive in: ' + self._deploy_root)
        else:
            logging.error('Extracting archive failed in: ' + self._deploy_root)
            extract_success = False

        return extract_success

    def _switch_local_venv(self) -> bool:
        venv_success = True
        venv_context_cmd = 'export WORKON_HOME=' + self._unpacked_build
        venv_context_args = venv_context_cmd.split()
        activate_venv_cmd = 'workon venv'
        activate_venv_args = activate_venv_cmd.split()

        local_shell = spur.LocalShell()
        try:
            local_shell.run(venv_context_args)
            logging.info('Switched venv WORKON_HOME: ' + self._unpacked_build)
        except spur.RunProcessError:
            logging.error('Switching venv WORKON_HOME failed: ' + self._unpacked_build)
            venv_success = False
        if venv_success:
            try:
                local_shell.run(activate_venv_args)
                logging.info('Activated venv with workon for build: ' + self._build_name)
            except spur.RunProcessError:
                logging.error('Activating venv with workon failed for build: ' + self._build_name)

        return venv_success

    def _execute_local_scripts(self) -> bool:
        execute_success = True
        local_shell = spur.LocalShell()
        for script in self._script_list:
            try:
                local_shell.run(['python3', script])
                logging.info('Executed script: ' + script)
            except spur.RunProcessError:
                logging.error('Failed to execute script: ' + script)
                execute_success = False
                break

        return execute_success
