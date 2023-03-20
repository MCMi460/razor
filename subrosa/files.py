# MCMi460 on Github
from . import *

def getAppPath(): # Credit to @HotaruBlaze
    applicationPath = os.path.expanduser('~/Documents/Razor')
    # Windows allows you to move your UserProfile subfolders, Such as Documents, Videos, Music etc.
    # However os.path.expanduser does not actually check and assumes it's in the default location.
    # This tries to correctly resolve the Documents path and fallbacks to default if it fails.
    if os.name == 'nt':
        try:
            import ctypes.wintypes
            CSIDL_PERSONAL = 5 # My Documents
            SHGFP_TYPE_CURRENT = 0 # Get current, not default value
            buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
            ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
            applicationPath = os.path.join(buf.value, 'Razor')
        except:
            pass
    return applicationPath

def getPath(path):
    try:
        root = sys._MEIPASS
    except Exception:
        root = os.path.abspath('.')

    return os.path.join(root, path)

appPath = getAppPath()

class FileSystem():
    def __init__(self, directory:str = 'sources/') -> None:
        assert isinstance(directory, str)# or...
        self.directory = os.path.join(appPath, directory)
        if not os.path.isdir(self.directory):
            os.makedirs(self.directory)

    def isFile(self, route:str) -> None:
        assert isinstance(route, str)
        file = self.directory + route
        return os.path.isfile(file)

    def isFolder(self, route:str) -> None:
        assert isinstance(route, str)
        folder = self.directory + route
        return os.path.isdir(folder)

    def createDirectory(self, route:str) -> None:
        assert isinstance(route, str)
        folder = self.directory + route
        if not os.path.isdir(folder):
            os.makedirs(folder)

    # `data` is not binary
    def createFile(self, route:str, data) -> None:
        assert isinstance(route, str)
        file = self.directory + route
        if os.path.isfile(file):
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
        assert os.path.isfile(file)

        with open(file, 'r') as fd:
            return fd.read()

    def deleteFile(self, route:str) -> None:
        assert isinstance(route, str)
        file = self.directory + route
        assert os.path.isfile(file)

        os.remove(file)
