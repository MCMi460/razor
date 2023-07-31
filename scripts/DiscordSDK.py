import os, sys, shutil, requests, zipfile

def useHook(text:str, hook, finished = False):
    print(text)
    if hook:
        hook(text, finished)

def installSDK(
        path:str,
        installPath:str,
        link:str,
        *,
        hook = None,
    ):
    try:
        url = link

        zipFile = os.path.join(installPath, 'sdk.zip')
        if os.path.isfile(zipFile):
            os.remove(zipFile)
        useHook('[Downloading SDK from %s...]' % url, hook)
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

        useHook('[Extracting SDK...]', hook)
        with zipfile.ZipFile(zipFile, 'r') as zip:
            zip.extractall(tempDir)

        for root, x, files in os.walk(tempDir):
            for file in files:
                if (file.endswith('.dll') and 'x86_64' in root) or (file.endswith('.dylib') and 'aarch64' in root):
                    shutil.copyfile(os.path.join(root, file), os.path.join(path, file))

        useHook('[Cleaning up install files...]', hook)

        shutil.rmtree(tempDir)
        os.remove(zipFile)

        # discord_game_sdk.dylib
        # discord_game_sdk.dll

        useHook('[Finished installing SDK!]', hook, True)
    except Exception as e:
        useHook(str(e), hook, 'Fail')

if __name__ == '__main__':
    installSDK('lib', '.', 'https://dl-game-sdk.discordapp.net/3.2.1/discord_game_sdk.zip')
