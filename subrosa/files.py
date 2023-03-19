# MCMi460 on Github
from . import *

class FileSystem():
    def __init__(self, directory:str = './sources/') -> None:
        assert isinstance(directory, str)# or...
        if not os.path.isdir(directory):
            os.mkdir(directory)
        self.directory = directory

    def isFile(self, path:str) -> None:
        assert isinstance(path, str)
        return os.path.isfile(path)

    def isFolder(self, path:str) -> None:
        assert isinstance(path, str)
        return os.path.isdir(path)

    def createDirectory(self, route:str) -> None:
        assert isinstance(route, str)
        folder = self.directory + route
        if not self.isFolder(folder):
            os.mkdir(folder)

    # `data` is not binary
    def createFile(self, route:str, data) -> None:
        assert isinstance(route, str)
        file = self.directory + route
        if self.isFile(file):
            os.remove(file)

        with open(file, 'w') as fd:
            fd.write(data)

    def appendFile(self, route:str, data) -> None:
        assert isinstance(route, str)
        file = self.directory + route

        with open(file, 'a') as fd:
            fd.write(data)

    def readFile(self, route:str) -> None:
        assert isinstance(route, str)
        file = self.directory + route
        assert self.isFile(file)

        with open(file, 'r') as fd:
            return fd.read()

    def deleteFile(self, route:str) -> None:
        assert isinstance(route, str)
        file = self.directory + route
        assert self.isFile(file)

        os.remove(file)
