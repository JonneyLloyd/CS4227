import logging
import os.path
from shutil import unpack_archive
import spur

from framework.interceptor import DeployInterceptor
from framework.context import DeployContext
from . import LocalDeployConfig


class LocalDeployInterceptor(DeployInterceptor[LocalDeployConfig]):
    """ Deploy an app locally - extract if packaged, run series of scripts """

    def pre_deploy(self, context: DeployContext) -> None:
        pre_deploy_success = False
        if self._validate_path(self.config.package_path) and self._validate_path(self.config.deploy_root):
            if self.config.packaged:
                if self._copy_packaged_build() and self._extract_build():
                    logging.info('Success: pre_deploy for extracted build: ' + self.config.build_name)
                    pre_deploy_success = True
            elif self._validate_path(self.config.unpacked_build):
                logging.info('Success: pre_deploy for unpackaged build: ' + self.config.build_name)
                pre_deploy_success = True
        if not pre_deploy_success:
            logging.error('Failure: pre_deploy for build: ' + self.config.build_name)

    def on_deploy(self, context: DeployContext) -> None:
        if self._switch_local_venv():
            logging.info('Success: on_deploy for build: ' + self.config.build_name)
        else:
            logging.error('Failure: on_deploy for build: ' + self.config.build_name)

    def post_deploy(self, context: DeployContext) -> None:
        post_deploy_success = True
        for script in self.config.script_list:
            if self._validate_path(script):
                logging.info('Found path to script: ' + script)
            else:
                logging.error('Failed to find path to script')
                post_deploy_success = False
        if post_deploy_success and self._execute_local_scripts():
            logging.info('Success: post_deploy script execution for build: ' + self.config.build_name)
        else:
            logging.error('Failure: post_deploy script execution for build: ' + self.config.build_name)

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
        copy_command = 'cp ' + self.config.package_path + " " + self.config.deploy_root
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
        if unpack_archive(self.config.package_path, self.config.deploy_root):
            logging.info('Extracted archive in: ' + self.config.deploy_root)
        else:
            logging.error('Extracting archive failed in: ' + self.config.deploy_root)
            extract_success = False

        return extract_success

    def _switch_local_venv(self) -> bool:
        venv_success = True
        venv_context_cmd = 'export WORKON_HOME=' + self.config.unpacked_build
        venv_context_args = venv_context_cmd.split()

        local_shell = spur.LocalShell()
        try:
            local_shell.run(venv_context_args)
            logging.info('Switched venv WORKON_HOME: ' + self.config.unpacked_build)
        except spur.RunProcessError:
            logging.error('Switching venv WORKON_HOME failed: ' + self.config.unpacked_build)
            venv_success = False
        if venv_success:
            try:
                local_shell.run(['sh', '-c', 'workon venv; deactivate'])
                logging.info('Tested venv activation for build: ' + self.config.build_name)
            except spur.RunProcessError:
                logging.error('Testing venv activation failed for build: ' + self.config.build_name)

        return venv_success

    def _execute_local_scripts(self) -> bool:
        execute_success = True
        local_shell = spur.LocalShell()
        for script in self.config.script_list:
            try:
                local_shell.run(['python3', script])
                logging.info('Executed script: ' + script)
            except spur.RunProcessError:
                logging.error('Failed to execute script: ' + script)
                execute_success = False
                break

        return execute_success
