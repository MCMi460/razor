# MCMi460 on Github
# Sets up FFMPEG (for Windows)
import os, shutil, requests, zipfile

def installFFMPEG(path:str):
    assert os.name == 'nt' # Windows install only
    
    if os.path.isfile('ffmpeg.zip'):
        os.remove('ffmpeg.zip')
    print('[Downloading FFMPEG...]')
    with open('ffmpeg.zip', 'wb+') as zip:
        request = requests.get('https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip')
        request.raise_for_status()
        zip.write(request.content)

    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    if os.path.exists('temp'):
        shutil.rmtree('temp')
    os.mkdir('temp')

    print('[Extracting FFMPEG...]')
    with zipfile.ZipFile('ffmpeg.zip', 'r') as zip:
        zip.extractall('temp')

    for root, x, files in os.walk('temp'):
        for file in files:
            if file.endswith('.exe'):
                shutil.copyfile(os.path.join(root, file), os.path.join(path, file))
    shutil.rmtree('temp')
    os.remove('ffmpeg.zip')

    # ffmpeg.exe
    # ffplay.exe
    # ffprobe.exe
