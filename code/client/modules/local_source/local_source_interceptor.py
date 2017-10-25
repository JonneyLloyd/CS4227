import os.path


class LocalSourceInterceptor:

    def __init__(self, sourcePath: str) -> None:
        self.sourcePath = sourcePath

    def validateSourcePath(self) -> bool:
        errorMsg = 'ERROR: Could not locate source path: '
        isValidPath = True
        if os.path.isdir(self.sourcePath):
            print('Located source path: ' + self.sourcePath)
        else:
            errorMsg += self.sourcePath
            print(errorMsg)
            isValidPath = False
        return isValidPath