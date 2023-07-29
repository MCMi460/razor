# MCMi460 on Github
# Sets up FFMPEG (for Windows)
import os, sys, shutil, requests, zipfile

def useHook(text:str, hook, finished = False):
    print(text)
    if hook:
        hook(text, finished)

def installFFMPEG(
        path:str,
        installPath:str,
        link:str,
        *,
        hook = None,
    ):
    try:
        assert os.name == 'nt' # Windows install only

        url = link

        zipFile = os.path.join(installPath, 'ffmpeg.zip')
        if os.path.isfile(zipFile):
            os.remove(zipFile)
        useHook('[Downloading FFMPEG from %s...]' % url, hook)
        with open(zipFile, 'wb+') as zip:
            request = requests.get(url)
            request.raise_for_status()
            zip.write(request.content)

        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)
        tempDir = os.path.join(installPath, 'temp')
        if os.path.exists(tempDir):
            shutil.rmtree(tempDir)
        os.mkdir(tempDir)

        useHook('[Extracting FFMPEG...]', hook)
        with zipfile.ZipFile(zipFile, 'r') as zip:
            zip.extractall(tempDir)

        for root, x, files in os.walk(tempDir):
            for file in files:
                if file.endswith('.exe'):
                    shutil.copyfile(os.path.join(root, file), os.path.join(path, file))

        useHook('[Cleaning up install files...]', hook)

        shutil.rmtree(tempDir)
        os.remove(zipFile)

        # ffmpeg.exe
        # ffplay.exe
        # ffprobe.exe

        useHook('[Finished installing FFMPEG!]', hook, True)
    except Exception as e:
        useHook(str(e), hook, 'Fail')

def installFFMPEGMac(
        path:str,
        installPath:str,
        links:list,
        *,
        hook = None,
    ):
    assert sys.platform.startswith('darwin') # Mac install only

    try:
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)
        import stat

        for link in links:
            url = link

            zipFile = os.path.join(installPath, 'ffmpeg.zip')
            if os.path.isfile(zipFile):
                os.remove(zipFile)
            useHook('[Downloading FFMPEG/FFPROBE from %s...]' % url, hook)
            with open(zipFile, 'wb+') as zip:
                request = requests.get(url)
                request.raise_for_status()
                zip.write(request.content)

            tempDir = os.path.join(installPath, 'temp')
            if os.path.exists(tempDir):
                shutil.rmtree(tempDir)
            os.mkdir(tempDir)

            useHook('[Extracting FFMPEG...]', hook)
            with zipfile.ZipFile(zipFile, 'r') as zip:
                zip.extractall(tempDir)

            for root, x, files in os.walk(tempDir):
                for file in files:
                    if file.startswith('ffmpeg') or file.startswith('ffprobe'):
                        shutil.copyfile(os.path.join(root, file), os.path.join(path, file))

                        st = os.stat(os.path.join(path, file))
                        os.chmod(os.path.join(path, file), st.st_mode | stat.S_IEXEC)

            useHook('[Cleaning up install files...]', hook)

            shutil.rmtree(tempDir)
            os.remove(zipFile)

        # ffmpeg
        # ffprobe

        useHook('[Finished installing FFMPEG!]', hook, True)

    except Exception as e:
        useHook(str(e), hook, 'Fail')
