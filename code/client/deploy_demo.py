from framework.pipeline.pipeline import Pipeline
from modules.local_source import LocalSourceInterceptor, LocalSourceConfig
from modules.python_build import PythonBuildInterceptor, PythonBuildConfig
from modules.zip_package import ZipPackageInterceptor, ZipPackageConfig
from modules.local_deploy import LocalDeployInterceptor, LocalDeployConfig


def main() -> None:
    """
    The following directory structure should be present on a UNIX machine before
    running the deploy demo:
    |-- /home/$USER/fw_test
      |-- src_dir
        |-- src_japp (this directory can be found in CS4227/code/src_japp)
          |-- requirements.txt
          |-- run.py
      |-- pre_build_dir
      |-- build_dir
      |-- pkg_dir
      |-- deploy_dir

    Make sure to replace path_prefix in path configs below
    """

    path_prefix = '/home/jay'

    pipeline = Pipeline()

    lsrc_config = LocalSourceConfig(path_prefix + '/fw_test/src_dir/src_japp', path_prefix + '/fw_test/pre_build_dir')
    build_config = PythonBuildConfig(path_prefix + '/fw_test/pre_build_dir/src_japp', path_prefix + '/fw_test/build_dir',
                                     'build_japp')
    pkg_config = ZipPackageConfig(path_prefix + '/fw_test/build_dir', 'build_japp', path_prefix + '/fw_test/pkg_dir/', 'zip')
    deploy_config = LocalDeployConfig(path_prefix + '/fw_test/pkg_dir/build_japp.zip', 'build_japp', path_prefix + '/fw_test/build_dir',
                                      [path_prefix + '/fw_test/build_dir/build_japp/app/run.py'], packaged=False)

    lsrc_interceptor = LocalSourceInterceptor()
    lsrc_interceptor.config = lsrc_config

    build_interceptor = PythonBuildInterceptor()
    build_interceptor.config = build_config

    pkg_interceptor = ZipPackageInterceptor()
    pkg_interceptor.config = pkg_config

    deploy_interceptor = LocalDeployInterceptor()
    deploy_interceptor.config = deploy_config

    lsrc_dispatcher = pipeline.source_dispatcher
    lsrc_dispatcher.register(lsrc_interceptor)

    build_dispatcher = pipeline.build_dispatcher
    build_dispatcher.register(build_interceptor)

    pkg_dispatcher = pipeline.package_dispatcher
    pkg_dispatcher.register(pkg_interceptor)

    deploy_dispatcher = pipeline.deploy_dispatcher
    deploy_dispatcher.register(deploy_interceptor)

    pipeline.execute()


if __name__ == '__main__':
    main()
