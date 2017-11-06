import os.path
import logging
import spur

from framework.interceptor import BuildInterceptor
from framework.context import BuildContext
from . import PythonBuildConfig


class PythonBuildInterceptor(BuildInterceptor[PythonBuildConfig]):

    def __init__(self, pre_build_path: str, build_root: str, build_name: str) -> None:
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

        Args:
            pre_build_path: Absolute path to directory containing sourced files
            build_root: Absolute path to root of directory containing finished builds
                        * This is also the default deployment directory *
            build_name: Name of build
        """
        self._pre_build_path = pre_build_path
        self._build_root = build_root
        self._build_name = build_name
        self._build_path = build_root.rstrip('\/') + '/' + build_name
        self._venv_path = self._build_path + '/venv'

    def pre_build(self, context: BuildContext) -> None:
        if self._validate_path(self._pre_build_path) and self._validate_path(self._build_path) \
           and self.create_build_dir() and self._move_source_for_build():
            logging.info('Success: pre_build for build ' + self._build_name)
        else:
            logging.error('Failure: pre_build for build ' + self._build_name)

    def on_build(self, context: BuildContext) -> None:
        if self._create_venv() and self._install_requirements():
            logging.info('Success: on_build for build: ' + self._build_name)
        else:
            logging.error('Failure: on_build for build: ' + self._build_name)

    def _validate_path(self, path: str) -> bool:
        is_valid_path = True
        if os.path.isabs(path):
            logging.info('Located ' + path.__name__ + ": " + path)
        else:
            logging.error('Could not locate ' + path.__name__ + ": " + path)
            is_valid_path = False

        return is_valid_path

    def _create_build_dir(self) -> bool:
        create_success = True
        mkdir_cmd = 'mkdir -p' + self._build_path + '/' + 'app'
        mkdir_args = mkdir_cmd.split()

        local_shell = spur.LocalShell()
        try:
            local_shell.run(mkdir_args)
            logging.info('Created build directory: ' + self._build_path)
        except spur.RunProcessError:
            logging.error('Creating build directory failed: ' + self._build_path)
            create_success = False

        return create_success

    def _copy_source_for_build(self) -> bool:
        move_success = True
        move_cmd = 'cp -r ' + self._pre_build_path + '/*' + self._build_path + '/app'
        move_args = move_cmd.split()

        local_shell = spur.LocalShell()
        try:
            local_shell.run(move_args)
            logging.info('Moving source to build directory succeeded: ' + move_cmd)
        except spur.RunProcessError:
            logging.error('Moving source to build directory failed: ' + move_cmd)
            move_success = False

        return move_success

    def _create_venv(self) -> bool:
        venv_success = True
        venv_context_cmd = 'export WORKON_HOME=' + self._build_path
        venv_context_args = venv_context_cmd.split()

        local_shell = spur.LocalShell()
        try:
            local_shell.run(venv_context_args)
            logging.info('Switched venv WORKON_HOME: ' + self._build_path)
        except spur.RunProcessError:
            logging.error('Switching venv WORKON_HOME failed: ' + self._build_path)
            venv_success = False
        if venv_success:
            try:
                local_shell.run(['mkvirtualenv', 'venv'])
                logging.info('Created virtual environment: ' + self._venv_path)
            except spur.RunProcessError:
                logging.error('Creating virtual environment failed: ' + self._venv_path)
                venv_success = False
        if venv_success:
            try:
                local_shell.run(['sh', '-c', 'workon venv; deactivate'])
                logging.info('Tested venv activation: ' + self._venv_path)
            except spur.RunProcessError:
                logging.error('Failed to test venv activation: ' + self._venv_path)
                venv_success = False

        return venv_success

    def _install_requirements(self) -> bool:
        install_success = True
        requirements_path = self._build_path + '/app/requirements.txt'
        pip_install_command = 'pip3 install -r ' + requirements_path

        local_shell = spur.LocalShell()
        try:
            local_shell.run(['sh', '-c', 'workon venv; ' + pip_install_command])
            logging.info('Installed pip requirements from ' + requirements_path)
        except spur.RunProcessError:
            logging.error('Failed to pip install dependencies from ' + requirements_path)
            install_success = False

        return install_success
