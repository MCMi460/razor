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
                # Format:
                # track_info
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
                'noplaylist': True,
            }

            fd.createDirectory('youtube')
            if fd.isFile('./sources/youtube/IDS.txt'):
                self.IDS = [ json.loads(a) for a in fd.readFile('youtube/IDS.txt').split('\n') ]
            self.CHECK_TITLE_LIST()

        def UPDATE_TITLE_LIST(self) -> None:
            fd.createFile('youtube/IDS.txt', '\n'.join(( json.dumps(a) for a in self.IDS )))

        def CHECK_TITLE_LIST(self) -> None:
            for song in self.IDS:
                if not fd.isFile('./sources/youtube/%s.mp3' % song['id']):
                    self.IDS.remove(song)
            self.UPDATE_TITLE_LIST()

        ### Standardized methods ###
        def DOWNLOAD_TRACK(self, id:str) -> str:
            assert isinstance(id, str)
            self.CHECK_TITLE_LIST()
            if id in ( a['id'] for a in self.IDS ):
                return os.path.abspath('./sources/youtube/%s.mp3' % id)
            url = 'https://youtube.com/watch?v=%s' % id
            response = track_info.copy()
            response['id'] = id
            for i in range(2):
                try:
                    with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                        info = ydl.extract_info(url, download = True)
                        response['id'] = info.get('id')
                        response['title'] = info.get('title')
                        response['artist'] = info.get('uploader')
                        response['thumbnail'] = info.get('thumbnail')
                        self.IDS.append(response)
                    self.UPDATE_TITLE_LIST()
                    return os.path.abspath('./sources/youtube/%s.mp3' % id)
                except:
                    pass
            raise Exception('failed to download track')

        def LIST_TRACKS(self) -> list:
            return list( a['id'] for a in self.IDS )

        def TRACK_INFO(self, id:str) -> dict:
            assert isinstance(id, str)
            for a in self.IDS:
                if id == a['id']:
                    return a
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

        def SEARCH(self, terms:str, cutoff:int = 10) -> list:
            assert isinstance(terms, str) and isinstance(cutoff, int)
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                return ydl.extract_info('ytsearch%s:%s' % (cutoff, terms), download = False)['entries']

    def PLAY_TRACK(PROVIDER:object, id:str):
        if not id in PROVIDER.IDS:
            PROVIDER.DOWNLOAD_TRACK(id)
        return vlc.MediaPlayer(PROVIDER.DOWNLOAD_TRACK(id))
