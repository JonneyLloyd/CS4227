import os.path
from shutil import make_archive
from os.path import dirname


class ZipPackageInterceptor():

    """ Input: Absolute path to root directory of build e.g. '/home/deployment/builds_dir/'
               Name of build e.g. 'python_build_v121'
               Absolute path to archived package e.g. '/home/deployment/package_dir/zip_package_v121' """
    def __init__(self, buildRoot: str, buildName: str, packagePath: str) -> None:
        self.buildRoot = buildRoot
        self.buildName = buildName
        self.packagePath = packagePath

    def validatePaths(self) -> bool:
        errorMsg = 'ERROR: Could not locate path(s):\n'
        isValidPath = True
        packageDir = dirname(self.packagePath)    # e.g. '/home/deployment/package_dir'
        buildPath = self.buildRoot + self.buildName    # e.g. '/home/deployment/builds_dir/python_build_v121'
        if os.path.isdir(buildPath):
            print('Located build path: ' + buildPath)
        else:
            errorMsg += 'Input - build path: ' + buildPath + '\n'
            isValidPath = False
        if os.path.isdir(packageDir):
            print('Located package directory: ' + packageDir)
        else:
            errorMsg += 'Output - package directory: ' + packageDir
            isValidPath = False
        if not isValidPath:
            print(errorMsg)
        return isValidPath

    def compressToZip(self) -> None:
            make_archive(
            self.packagePath,
            'zip',
            root_dir=self.buildRoot,
            base_dir=self.buildName)

    def compressToGztar(self) -> None:
        make_archive(
            self.packagePath,
            'gztar',
            root_dir=self.buildRoot,
            base_dir=self.buildName)

    def compressToXztar(self) -> None:
        make_archive(
            self.packagePath,
            'xztar',
            root_dir=self.buildRoot,
            base_dir=self.buildName)

    def archiveToTar(self) -> None:
        make_archive(
            self.packagePath,
            'tar',
            root_dir = self.buildRoot,
            base_dir = self.buildName)

