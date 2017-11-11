import logging
import os.path
from shutil import unpack_archive
import spur
from framework.interceptor import DeployInterceptor
from framework.context import DeployContext
from . import LocalDeployConfig
logging.basicConfig(level=logging.INFO)


class LocalDeployInterceptor(DeployInterceptor[LocalDeployConfig]):
    """ Deploy an app locally - extract if packaged, run series of scripts """

    def pre_deploy(self, context: DeployContext) -> None:
        context.set_state({'pre_deploy': 'in progress', 'on_deploy': 'waiting'})
        pre_deploy_success = False
        if self._validate_path(self.config.deploy_root, False):
            if self.config.packaged and self._validate_path(self.config.package_path, True):
                """ If packaged, copy packaged build to deploy directory and extract """
                if self._validate_path(self.config.unpacked_build, False):
                    self._remove_existing_build()
                    if self._copy_packaged_build() and self._extract_build():
                        logging.info('local_deploy_interceptor: Success: pre_deploy for extracted build: ' + self.config.build_name)
                        pre_deploy_success = True
            elif self._validate_path(self.config.unpacked_build, False):
                """ If not packaged, build will be already located in deploy directory """
                logging.info('local_deploy_interceptor: Success: pre_deploy for unpackaged build: ' + self.config.build_name)
                pre_deploy_success = True
        if not pre_deploy_success:
            logging.error('local_deploy_interceptor: Failure: pre_deploy for build: ' + self.config.build_name)
            context.set_state({'pre_deploy': 'failed', 'on_deploy': 'waiting'})
        else:
            context.set_state({'pre_deploy': 'successful', 'on_deploy': 'waiting'})

    def on_deploy(self, context: DeployContext) -> None:
        context.set_state({'pre_deploy': 'successful', 'on_deploy': 'in progress'})
        on_deploy_success = True
        for script in self.config.script_list:
            if self._validate_path(script, True):
                logging.info('local_deploy_interceptor: Found path to script: ' + script)
            else:
                logging.error('local_deploy_interceptor: Failed to find path to script')
                on_deploy_success = False
        if on_deploy_success and self._execute_local_scripts():
            logging.info('local_deploy_interceptor: Success: on_deploy script execution for build: ' + self.config.build_name)
            context.set_state({'pre_deploy': 'successful', 'on_deploy': 'successful'})
        else:
            logging.error('local_deploy_interceptor: Failure: on_deploy script execution for build: ' + self.config.build_name)
            context.set_state({'pre_deploy': 'successful', 'on_deploy': 'failed'})

    def _validate_path(self, path: str, is_file: bool) -> bool:
        """ The is_file flag determines if validating a file or directory path """
        is_valid_path = True
        if is_file and not os.path.isfile(path):
            is_valid_path = False
        elif not is_file and not os.path.isdir(path):
            is_valid_path = False
        if is_valid_path:
            logging.info('local_deploy_interceptor: Located path: ' + path)
        else:
            logging.error('local_deploy_interceptor: Could not locate path: ' + path)

        return is_valid_path

    def _remove_existing_build(self):
        """ If extracting a packaged build, we want to make sure the existing unpackaged
            build in the same directory is not present """
        local_shell = spur.LocalShell()
        try:
            local_shell.run(['sh', '-c', 'rm -r ' + self.config.unpacked_build])
            logging.info('local_deploy_interceptor: Removed existing build in build_dir before extracting packaged build')
        except spur.RunProcessError:
            logging.error('local_deploy_interceptor: Failed to remove existing build')

    def _copy_packaged_build(self) -> bool:
        copy_success = True
        copy_command = 'cp ' + self.config.package_path + ' ' + self.config.deploy_root

        local_shell = spur.LocalShell()
        try:
            local_shell.run(['sh', '-c', copy_command])
            logging.info('local_deploy_interceptor: Copied packaged build for deployment: ' + copy_command)
        except spur.RunProcessError:
            logging.error('local_deploy_interceptor: Copying packaged build for deployment failed: ' + copy_command)
            copy_success = False

        return copy_success

    def _extract_build(self) -> bool:
        extract_success = True
        try:
            unpack_archive(self.config.package_path, self.config.deploy_root)
            logging.info('local_deploy_interceptor: Extracted archive in: ' + self.config.deploy_root)
        except Exception as e:
            logging.error('local_deploy_interceptor: Extracting archive failed in: ' + self.config.deploy_root)
            extract_success = False

        return extract_success

    def _execute_local_scripts(self) -> bool:
        execute_success = True
        local_shell = spur.LocalShell()
        for script in self.config.script_list:
            try:
                local_shell.run(['sh', '-c', 'cd ' + self.config.venv_bin_path + '; python3 ' + script])
                logging.info('local_deploy_interceptor: Executed script: ' + script)
            except spur.RunProcessError:
                logging.error('local_deploy_interceptor: Failed to execute script: ' + script)
                execute_success = False
                break

        return execute_success
