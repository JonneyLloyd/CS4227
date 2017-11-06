import os.path
import logging
import spur
import venv
from framework.interceptor import BuildInterceptor
from framework.context import BuildContext

from . import PythonBuildConfig


class PythonBuildInterceptor(BuildInterceptor[PythonBuildConfig]):

    def __init__(self, pre_build_path: str, build_root: str, build_name: str) -> None:
        self._pre_build_path = pre_build_path
        self._build_root = build_root
        self._build_name = build_name
        self._build_path = build_root + '/' + build_name
        self._move_command = 'mv ' + self._pre_build_path + '/*' + self._build_path + '/app'

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
        if os.path.isdir(self._source_path):
            logging.info('Located ' + path.__name__ + ": " + path)
        else:
            logging.error('Could not locate ' + path.__name__ + ": " + path)
            is_valid_path = False

        return is_valid_path

    def create_build_dir(self) -> bool:
        create_success = True
        local_shell = spur.LocalShell()

        result = local_shell.run('mkdir -p' + self._build_path + '/' + 'app')
        if result.return_code != 0:
            logging.error('Creating build directory:\n' + result.stderr_output)
            create_success = False
        else:
            logging.info('Created build directory:\n' + result.output)

        return create_success

    def _move_source_for_build(self) -> bool:
        move_success = True
        local_shell = spur.LocalShell()

        result = local_shell.run(self._move_command)
        if result.return_code != 0:
            logging.error('Moving source to build directory failed:\n' + result.stderr_output)
            move_success = False
        else:
            logging.info('Moving source to build directory succeeded:\n' + result.output)

        return move_success

    def _create_venv(self) -> bool:
        venv_success = True
        venv_path = self._build_path + '/venv'
        if venv.create(venv_path):
            logging.info('Created venv in: ' + self._build_path)
        else:
            venv_success = False
            logging.error('Unable to create venv in: ' + self._build_path)

        return venv_success

    def _install_requirements(self) -> bool:
        install_success = True
        venv_activate_path = 'source ' + self._build_path + '/venv/bin/activate'
        local_shell = spur.LocalShell()

        result = local_shell.run(venv_activate_path)
        if result.return_code != 0:
            install_success = False
            logging.error('Unable to source venv:\n' + result.stderr_output)
        else:
            logging.info('Sourced venv:\n' + venv_activate_path)
        if install_success:
            result = local_shell.run('pip3 install -r ' + self._build_path + '/app/requirements.txt')
            if result.return_code != 0:
                install_success = False
                logging.error('Failed to pip install dependencies from requirements.txt:\n'
                              + result.stderr_output)
            else:
                logging.info('Success: installed pip requirements:\n' + result.output)
                local_shell.run('deactivate')

        return install_success
