import os.path
import logging
import spur

from framework.interceptor import BuildInterceptor
from framework.context import BuildContext
from . import PythonBuildConfig
logging.basicConfig(level=logging.INFO)


class PythonBuildInterceptor(BuildInterceptor[PythonBuildConfig]):
    """
    Build a python application - create virtual environment and install dependencies

    Creates a directory structure in finished builds directory:
        |-- build_root    (AKA deployment directory)
          |-- build_name
            |-- app       (contains app source files)
            |-- venv      (contains built virtual env)

    Since finished builds directory is also the deployments directory, deployment
    can be performed locally directly after build (without packaging). In other cases,
    the build can be packaged with archive/compression and copied to the corresponding
    deployments directory on a remote host.
    """

    def pre_build(self, context: BuildContext) -> None:
        if self._validate_path(self.config.pre_build_path) \
           and self._validate_path(self.config.build_path) \
           and self._create_build_dir() and self._copy_source_for_build():
            logging.info('Success: pre_build for build ' + self.config.build_name)
        else:
            logging.error('Failure: pre_build for build ' + self.config.build_name)

    def on_build(self, context: BuildContext) -> None:
        if self._create_venv() and self._install_requirements():
            logging.info('Success: on_build for build: ' + self.config.build_name)
        else:
            logging.error('Failure: on_build for build: ' + self.config.build_name)

    def _validate_path(self, path: str) -> bool:
        is_valid_path = True
        if os.path.isdir(path):
            logging.info('Located path: ' + path)
        else:
            logging.error('Could not locate path: ' + path)
            is_valid_path = False

        return is_valid_path

    def _create_build_dir(self) -> bool:
        create_success = True
        mkdir_cmd = 'mkdir -p' + self.config.build_path + '/' + 'app'
        mkdir_args = mkdir_cmd.split()

        local_shell = spur.LocalShell()
        try:
            local_shell.run(mkdir_args)
            logging.info('Created build directory: ' + self.config.build_path)
        except spur.RunProcessError:
            logging.error('Creating build directory failed: ' + self.config.build_path)
            create_success = False

        return create_success

    def _copy_source_for_build(self) -> bool:
        copy_success = True
        copy_cmd = 'cp -r ' + self.config.pre_build_path + '/*' + self.config.build_path + '/app'
        copy_args = copy_cmd.split()

        local_shell = spur.LocalShell()
        try:
            local_shell.run(copy_args)
            logging.info('Moving source to build directory succeeded: ' + copy_cmd)
        except spur.RunProcessError:
            logging.error('Moving source to build directory failed: ' + copy_cmd)
            copy_success = False

        return copy_success

    def _create_venv(self) -> bool:
        venv_success = True
        venv_context_cmd = 'export WORKON_HOME=' + self.config.build_path
        venv_context_args = venv_context_cmd.split()

        local_shell = spur.LocalShell()
        try:
            local_shell.run(venv_context_args)
            logging.info('Switched venv WORKON_HOME: ' + self.config.build_path)
        except spur.RunProcessError:
            logging.error('Switching venv WORKON_HOME failed: ' + self.config.build_path)
            venv_success = False
        if venv_success:
            try:
                local_shell.run(['mkvirtualenv', 'venv'])
                logging.info('Created virtual environment: ' + self.config.venv_path)
            except spur.RunProcessError:
                logging.error('Creating virtual environment failed: ' + self.config.venv_path)
                venv_success = False
        if venv_success:
            try:
                local_shell.run(['sh', '-c', 'workon venv; deactivate'])
                logging.info('Tested venv activation: ' + self.config.venv_path)
            except spur.RunProcessError:
                logging.error('Failed to test venv activation: ' + self.config.venv_path)
                venv_success = False

        return venv_success

    def _install_requirements(self) -> bool:
        install_success = True
        requirements_path = self.config.build_path + '/app/requirements.txt'
        pip_install_command = 'pip3 install -r ' + requirements_path

        local_shell = spur.LocalShell()
        try:
            local_shell.run(['sh', '-c', 'workon venv; ' + pip_install_command])
            logging.info('Installed pip requirements from ' + requirements_path)
        except spur.RunProcessError:
            logging.error('Failed to pip install dependencies from ' + requirements_path)
            install_success = False

        return install_success
