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
        context.set_state({'pre_build': 'in progress', 'on_build': 'waiting'})
        if self._validate_path(self.config.pre_build_path):
            self.remove_existing_build(self.config.build_path)
            if self._create_build_dir() and self._copy_source_for_build():
                logging.info('python_build_interceptor: Success: pre_build for build ' + self.config.build_name)
                context.set_state({'pre_build': 'successful', 'on_build': 'waiting'})
            else:
                logging.error('python_build_interceptor: Failure: pre_build for build ' + self.config.build_name)
                context.set_state({'pre_build': 'failed', 'on_build': 'waiting'})

    def on_build(self, context: BuildContext) -> None:
        context.set_state({'pre_build': 'successful', 'on_build': 'in progress'})
        if self._create_venv() and self._install_requirements():
            logging.info('python_build_interceptor: Success: on_build for build: ' + self.config.build_name)
            context.set_state({'pre_build': 'successful', 'on_build': 'successful'})
        else:
            logging.error('python_build_interceptor: Failure: on_build for build: ' + self.config.build_name)
            context.set_state({'pre_build': 'successful', 'on_build': 'failed'})

    def _validate_path(self, path: str) -> bool:
        is_valid_path = True
        if os.path.isdir(path):
            logging.info('python_build_interceptor: Located path: ' + path)
        else:
            logging.error('python_build_interceptor: Could not locate path: ' + path)
            is_valid_path = False

        return is_valid_path

    def _create_build_dir(self) -> bool:
        create_success = True
        mkdir_cmd = 'mkdir -p ' + self.config.build_path + '/' + 'app'
        mkdir_args = mkdir_cmd.split()

        local_shell = spur.LocalShell()
        try:
            local_shell.run(mkdir_args)
            logging.info('python_build_interceptor: Created build directory: ' + self.config.build_path)
        except spur.RunProcessError:
            logging.error('python_build_interceptor: Creating build directory failed: ' + self.config.build_path)
            create_success = False

        return create_success

    def _copy_source_for_build(self) -> bool:
        copy_success = True
        copy_cmd = 'cp -r ' + self.config.pre_build_path + '/* ' + self.config.build_path + '/app'

        local_shell = spur.LocalShell()
        try:
            local_shell.run(['sh', '-c', copy_cmd])
            logging.info('python_build_interceptor: Copying source to build directory succeeded: ' + copy_cmd)
        except spur.RunProcessError:
            logging.error('python_build_interceptor: Copying source to build directory failed: ' + copy_cmd)
            copy_success = False

        return copy_success

    def _create_venv(self) -> bool:
        venv_success = True
        local_shell = spur.LocalShell()
        try:
            local_shell.run(['sh', '-c', 'python3 -m venv --copies ' + self.config.venv_path])
            logging.info('python_build_interceptor: Created virtual environment: ' + self.config.venv_path)
        except spur.RunProcessError:
            logging.error('python_build_interceptor: Creating virtual environment failed: ' + self.config.venv_path)
            venv_success = False

        return venv_success

    def _install_requirements(self) -> bool:
        install_success = True
        requirements_path = self.config.build_path + '/app/requirements.txt'
        pip_install_command = self.config.python_path + ' -m pip install -r ' + requirements_path

        local_shell = spur.LocalShell()
        try:
            local_shell.run(['sh', '-c', pip_install_command])
            logging.info('python_build_interceptor: Installed pip requirements from ' + requirements_path)
        except spur.RunProcessError:
            logging.error('python_build_interceptor: Failed to pip install dependencies from ' + requirements_path)
            install_success = False

        return install_success
