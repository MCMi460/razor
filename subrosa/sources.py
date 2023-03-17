# MCMi460 on Github
from . import *

track_info = {
    'title': '',
    'artist': '',
    'thumbnail': '',
    'id': '',
}

class Source:
    class Youtube():
        def __init__(self) -> None:
            self.IDS = [
                # Default:
                # NONE
            ]
            self.ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': './sources/youtube/%(id)s.%(ext)s',
                'quiet': True,
            }

            fd.createDirectory('youtube')
            if fd.isFile('./sources/youtube/IDS.txt'):
                self.IDS = fd.readFile('youtube/IDS.txt').split('\n')
            self.UPDATE_TITLE_LIST()

        def UPDATE_TITLE_LIST(self) -> None:
            fd.createFile('youtube/IDS.txt', '\n'.join(self.IDS))

        def CHECK_TITLE_LIST(self) -> None:
            for id in self.IDS:
                if not fd.isFile('./sources/youtube/%s.mp3' % id):
                    self.IDS.remove(id)
            self.UPDATE_TITLE_LIST()

        ### Standardized methods ###
        def DOWNLOAD_TRACK(self, id:str) -> str:
            assert isinstance(id, str)
            self.CHECK_TITLE_LIST()
            if id in self.IDS:
                return os.path.abspath('./sources/youtube/%s.mp3' % id)
            url = 'https://youtube.com/watch?v=%s' % id
            for i in range(2):
                try:
                    with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                        ydl.download([url])
                    self.IDS.append(id)
                    self.UPDATE_TITLE_LIST()
                    return os.path.abspath('./sources/youtube/%s.mp3' % id)
                except:
                    pass
            raise Exception('failed to download track')

        def LIST_TRACKS(self) -> list:
            return self.IDS

        def TRACK_INFO(self, id:str) -> dict:
            assert isinstance(id, str)
            url = 'https://youtube.com/watch?v=%s' % id
            response = track_info.copy()
            response['id'] = id
            for i in range(2):
                try:
                    with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                        info = ydl.extract_info(url, download = False)
                        response['id'] = info.get('id')
                        response['title'] = info.get('title')
                        response['artist'] = info.get('uploader')
                        response['thumbnail'] = info.get('thumbnail')
                    break
                except:
                    pass
            return response

    def PLAY_TRACK(PROVIDER:object, id:str):
        if not id in PROVIDER.IDS:
            PROVIDER.DOWNLOAD_TRACK(id)
        playsound.playsound(PROVIDER.DOWNLOAD_TRACK(id))
