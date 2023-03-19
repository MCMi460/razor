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
                'writethumbnail': True,
            }

            fd.createDirectory('youtube')
            if fd.isFile('./sources/youtube/IDS.txt'):
                try:
                    self.IDS = [ json.loads(a) for a in fd.readFile('youtube/IDS.txt').split('\n') ]
                except:
                    self.IDS = []
            self.CHECK_TITLE_LIST()

        def UPDATE_TITLE_LIST(self) -> None:
            fd.createFile('youtube/IDS.txt', '\n'.join(( json.dumps(a) for a in self.IDS )))

        def CHECK_TITLE_LIST(self) -> None:
            for song in self.IDS:
                if not fd.isFile('./sources/youtube/%s.mp3' % song['id']):
                    self.IDS.remove(song)
            self.UPDATE_TITLE_LIST()

        ### Standardized methods ###
        def DOWNLOAD_TRACK(self, id:str, hook = None) -> str:
            assert isinstance(id, str)
            self.CHECK_TITLE_LIST()
            if id in ( a['id'] for a in self.IDS ):
                return os.path.abspath('./sources/youtube/%s.mp3' % id)
            url = 'https://youtube.com/watch?v=%s' % id
            response = track_info.copy()
            response['id'] = id
            opts = self.ydl_opts.copy()
            if hook:
                opts['progress_hooks'] = [hook]
            for i in range(2):
                try:
                    with youtube_dl.YoutubeDL(opts) as ydl:
                        info = ydl.extract_info(url, download = True)
                        response['id'] = info.get('id')
                        response['title'] = info.get('title')
                        response['artist'] = info.get('uploader')
                        response['thumbnail'] = info.get('thumbnail')
                        self.IDS.append(response)
                    if not response['thumbnail'].endswith('jpg'):
                        image = PIL.Image.open('./sources/youtube/%s.%s' % (response['id'], response['thumbnail'].split('.')[-1])).convert('RGB')
                        image.save('./sources/youtube/%s.jpg' % response['id'], 'jpeg')
                        fd.deleteFile('youtube/%s.%s' % (response['id'], response['thumbnail'].split('.')[-1]))
                    self.UPDATE_TITLE_LIST()
                    return os.path.abspath('./sources/youtube/%s.mp3' % id)
                except:
                    pass
            raise Exception('failed to download track')

        def LIST_TRACKS(self) -> list:
            return list( a['id'] for a in self.IDS )

        def LIST_TRACKS_INFO(self) -> list:
            return self.IDS

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

        def SEARCH(self, terms:str, *, cutoff:int = 10) -> list:
            assert isinstance(terms, str) and isinstance(cutoff, int)
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                return ydl.extract_info('ytsearch%s:%s' % (cutoff, terms), download = False)['entries']

        def DELETE_TRACK(self, id:str) -> None:
            assert isinstance(id, str)
            for song in self.IDS:
                if song['id'] == id:
                    self.IDS.remove(song)
                    for ext in ('mp3', 'jpg'):
                        fd.deleteFile('youtube/%s.%s' % (song['id'], ext))

    def PLAY_TRACK(PROVIDER:object, id:str):
        return vlc.MediaPlayer(PROVIDER.DOWNLOAD_TRACK(id))
