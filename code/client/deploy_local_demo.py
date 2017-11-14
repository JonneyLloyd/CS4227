from framework.pipeline.pipeline import Pipeline
from modules.local_source import LocalSourceInterceptor, LocalSourceConfig
from modules.python_build import PythonBuildInterceptor, PythonBuildConfig
from modules.zip_package import ZipPackageInterceptor, ZipPackageConfig
from modules.local_deploy import LocalDeployInterceptor, LocalDeployConfig


def main() -> None:
    """
    The following directory structure should be present on a UNIX machine before
    running the deploy demo:
    |-- /deployments
      |-- pre_build_dir
      |-- build_dir
      |-- pkg_dir
      |-- deploy_dir

    The code source must also be available locally with a similar structure:
    |-- some_dir
      |-- src_japp (this directory can be found in CS4227/code/src_japp)
        |-- requirements.txt
        |-- run.py

    """

    path_prefix = '/deployments'

    pipeline = Pipeline()

    lsrc_config = LocalSourceConfig('/home/oligavin/workspace/Y4Sem1/CS4227SoftwareDesignAndArchitecture/test_flask_app',
                                    f'{path_prefix}/pre_build_dir')
    build_config = PythonBuildConfig(f'{path_prefix}/pre_build_dir/test_flask_app',
                                     f'{path_prefix}/build_dir',
                                     'build_japp')
    pkg_config = ZipPackageConfig(f'{path_prefix}/build_dir', 'build_japp', f'{path_prefix}/pkg_dir/', 'zip')
    deploy_config = LocalDeployConfig(f'{path_prefix}/pkg_dir/build_japp.zip', 'build_japp', f'{path_prefix}/build_dir',
                                      [f'{path_prefix}/build_dir/build_japp/app/run.py'], packaged=False)

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
