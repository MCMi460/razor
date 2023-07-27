# MCMi460 on Github
from . import *

track_info = {
    'title': '',
    'artist': '',
    'thumbnail': '',
    'id': '',
}

playlist_info = {
    'name': '',
    'songs': [], # List of `track_info`s
    'thumbnail': '', # Can be None. If None, then default playlist logo will appear.
                     # Standardized to be a local file, preferably an absolute path.
                     # Can be a URL if playlist is not saved.
    'id': '', # Either a random number with a leading tilda (Razor playlist),
              # or an ID for a Youtube playlist (cannot be a "Mix")
    'description': '', # Either user-inputted or taken from Youtube
}

class Source:
    class Youtube():
        def __init__(self, *, sendUpdate = None) -> None:
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
                }, {
                    'format': 'jpg',
                    'key': 'FFmpegThumbnailsConvertor',
                    'when': 'before_dl'}],
                'outtmpl': os.path.join(fd.directory, 'youtube/%(id)s.%(ext)s'),
                'quiet': True,
                'noplaylist': True,
                'writethumbnail': True,
                'no_continue': True,
                'ignoreerrors': True,
            }
            if os.name == 'nt':
                self.ydl_opts['ffmpeg_location'] = getPath('ffmpeg')
            self.setupFinish = False

            fd.createDirectory('youtube')
            if fd.isFile('youtube/IDS.txt'):
                try:
                    self.IDS = [ json.loads(a) for a in fd.readFile('youtube/IDS.txt').split('\n') ]
                except:
                    self.IDS = []
            self.CHECK_TITLE_LIST(sendUpdate = sendUpdate)

        def UPDATE_TITLE_LIST(self) -> None:
            fd.createFile('youtube/IDS.txt', '\n'.join(( json.dumps(a) for a in self.IDS )))

        def CHECK_TITLE_LIST(self, *, sendUpdate = None) -> None:
            IDS = self.IDS
            self.IDS = []
            reDownload = []
            for song in IDS:
                if not fd.isFile('youtube/%s.mp3' % song['id']):
                    reDownload.append(song)
                else:
                    self.IDS.append(song)
            def start():
                for song in reDownload:
                    try:
                        self.DOWNLOAD_TRACK(song['id'], check_list = False, sendUpdate = sendUpdate)
                    except Exception as e:
                        #print('FAIL')
                        #print(e)
                        pass
                    time.sleep(1)
                self.setupFinish = True
            if len(reDownload) > 0:
                threading.Thread(target = start, daemon = True).start()
            else:
                self.setupFinish = True
            self.UPDATE_TITLE_LIST()

        ### Standardized methods ###
        def DOWNLOAD_TRACK(self, id:str, *, hook = None, check_list = True, sendUpdate = None) -> str:
            assert isinstance(id, str)
            if check_list:
                self.CHECK_TITLE_LIST()
                if id in ( a['id'] for a in self.IDS ):
                    return os.path.abspath(os.path.join(fd.directory, 'youtube/%s.mp3' % id))
            url = 'https://youtube.com/watch?v=%s' % id
            response = track_info.copy()
            response['id'] = id
            opts = self.ydl_opts.copy()
            if hook:
                opts['progress_hooks'] = [hook]
            for i in range(5):
                try:
                    with yt_dlp.YoutubeDL(opts) as ydl:
                        info = ydl.extract_info(url, download = True)
                        response['id'] = info.get('id')
                        response['title'] = info.get('title')
                        response['artist'] = info.get('uploader')
                        response['thumbnail'] = info.get('thumbnail')
                    self.IDS.append(response)
                    self.UPDATE_TITLE_LIST()
                    if sendUpdate:
                        sendUpdate()
                    return os.path.abspath(os.path.join(fd.directory, 'youtube/%s.mp3' % id))
                except Exception as e:
                    #print(traceback.format_exc().strip())
                    pass
            if not check_list:
                for i in range(len(self.IDS)):
                    if self.IDS[i]['id'] == id:
                        self.IDS.pop(i)
                        break
            if sendUpdate:
                sendUpdate()
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
                    with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
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
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                return ydl.extract_info('ytsearch%s:%s' % (cutoff, terms), download = False)['entries']

        def DELETE_TRACK(self, id:str) -> None:
            assert isinstance(id, str)
            for song in self.IDS:
                if song['id'] == id:
                    self.IDS.remove(song)
                    for ext in ('mp3', 'jpg'):
                        fd.deleteFile('youtube/%s.%s' % (song['id'], ext))
                    self.UPDATE_TITLE_LIST()

        def GET_PLAYLIST(self, id:str) -> list:
            with yt_dlp.YoutubeDL(dict(self.ydl_opts, **{
                    'extract_flat': 'in_playlist',
                }
            )) as ydl:
                response = ydl.extract_info(id, download = False)
            playlist = playlist_info.copy()
            playlist['id'] = response['id']
            playlist['name'] = response.get('title')
            playlist['description'] = response.get('description', '')
            playlist['thumbnail'] = response.get('thumbnails', [{},])[-1].get('url', '')
            for song in response['entries']:
                track = track_info.copy()
                track['id'] = song.get('id')
                track['title'] = song.get('title')
                track['artist'] = song.get('uploader')
                track['thumbnail'] = song.get('thumbnails', [{},])[-1].get('url', '')
                playlist['songs'].append(track)
            return playlist

    def PLAY_TRACK(PROVIDER:object, id:str):
        return Audio.Player(PROVIDER.DOWNLOAD_TRACK(id))
