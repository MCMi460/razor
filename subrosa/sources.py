# MCMi460 on Github
from . import *

track_info = {
    'title': '',
    'artist': '',
    'thumbnail': '',
    'id': '',
}

playlist_info = {
    'playlist': True,
    'title': '',
    'artist': '',
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
            self.LISTS = [
                # Default:
                # NONE
                # Format:
                # playlist_info
            ]
            self.ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    },
                    {
                        'format': 'jpg',
                        'key': 'FFmpegThumbnailsConvertor',
                        'when': 'before_dl',
                    }
                ],
                'outtmpl': os.path.join(fd.directory, 'youtube/%(id)s.%(ext)s'),
                'quiet': True,
                'noplaylist': True,
                'writethumbnail': True,
                'no_continue': True,
                'ignoreerrors': True,
            }
            self.setupFinish = True

            fd.createDirectory('youtube')
            if fd.isFile('youtube/IDS.txt'):
                try:
                    self.IDS = [ json.loads(a) for a in fd.readFile('youtube/IDS.txt').split('\n') ]
                except:
                    self.IDS = []
            if fd.isFile('youtube/LISTS.txt'):
                try:
                    self.LISTS = [ json.loads(a) for a in fd.readFile('youtube/LISTS.txt').split('\n') ]
                except:
                    self.LISTS = []
            self.CHECK_TITLE_LIST(sendUpdate = sendUpdate)

        def UPDATE_TITLE_LIST(self) -> None:
            fd.createFile('youtube/IDS.txt', '\n'.join(( json.dumps(a) for a in self.IDS )))
            fd.createFile('youtube/LISTS.txt', '\n'.join(( json.dumps(a) for a in self.LISTS )))

        def CHECK_TITLE_LIST(self, *, sendUpdate = None) -> None:
            IDS = self.IDS
            reDownload = []
            rePlaylists = []
            for playlist in self.LISTS:
                if not fd.isFile('youtube/%s.jpg' % playlist['id']):
                    rePlaylists.append(playlist)
                for song in playlist['songs']:
                    if not song['id'] in [ song['id'] for song in IDS ]:
                        IDS = [song] + IDS
            for song in IDS:
                if not fd.isFile('youtube/%s.mp3' % song['id']) or not fd.isFile('youtube/%s.jpg' % song['id']):
                    reDownload.append(song)
            def start():
                for playlist in rePlaylists:
                    try:
                        self.ADD_PLAYLIST(playlist['id'], update = False)
                        sendUpdate()
                    except:
                        pass
                for song in reDownload:
                    try:
                        self.DOWNLOAD_TRACK(song['id'], check_list = False, sendUpdate = sendUpdate)
                    except Exception as e:
                        #print('FAIL')
                        #print(e)
                        pass
                    time.sleep(1)
                self.setupFinish = True
            if len(reDownload) > 0 or len(rePlaylists) > 0:
                if self.setupFinish:
                    self.setupFinish = False
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
            for i in range(2):
                try:
                    with yt_dlp.YoutubeDL(opts) as ydl:
                        info = ydl.extract_info(url, download = True)
                        response['id'] = info.get('id')
                        response['title'] = info.get('title')
                        response['artist'] = info.get('uploader')
                        response['thumbnail'] = info.get('thumbnail')
                    assert fd.isFile('youtube/%s.mp3' % id)
                    if not id in [ s['id'] for s in self.IDS ]:
                        self.IDS.append(response)
                        self.UPDATE_TITLE_LIST()
                    if sendUpdate:
                        sendUpdate()
                    return os.path.abspath(os.path.join(fd.directory, 'youtube/%s.mp3' % id))
                except Exception as e:
                    raise e
            if not check_list:
                for i in range(len(self.IDS)):
                    if self.IDS[i]['id'] == id:
                        self.IDS.pop(i)
                        break
            if sendUpdate:
                sendUpdate()
            raise Exception('failed to download track')

        def LIST_TRACKS(self, GUI:bool = False) -> list:
            IDS = self.IDS
            if GUI:
                IDS = []
                for song in self.IDS:
                    id = song['id']
                    if not fd.isFile('youtube/%s.mp3' % id) or not fd.isFile('youtube/%s.jpg' % id):
                        self.CHECK_TITLE_LIST()
                    else:
                        IDS.append(song)
            return list( a['id'] for a in IDS )

        def LIST_TRACKS_INFO(self, GUI:bool = False) -> list:
            IDS = self.IDS
            if GUI:
                IDS = []
                for song in self.IDS:
                    id = song['id']
                    if not fd.isFile('youtube/%s.mp3' % id) or not fd.isFile('youtube/%s.jpg' % id):
                        self.CHECK_TITLE_LIST()
                    else:
                        IDS.append(song)
            return IDS

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

        def ADD_PLAYLIST(self, id:str, *, sendUpdate = None, update = True) -> None:
            assert isinstance(id, str)
            with yt_dlp.YoutubeDL(dict(self.ydl_opts, **{
                    'extract_flat': 'in_playlist',
                }
            )) as ydl:
                response = ydl.extract_info(id, download = False)
            playlist = playlist_info.copy()
            playlist['id'] = response['id']
            playlist['title'] = response.get('title')
            playlist['artist'] = response.get('uploader_id')
            playlist['description'] = response.get('description', '')
            playlist['thumbnail'] = response.get('thumbnails', [{},])[-1].get('url', '')
            for song in response['entries']:
                if song['title'] == '[Private video]':
                    print('[SKIPPING PRIVATE VIDEO]')
                    continue
                track = track_info.copy()
                track['id'] = song.get('id')
                track['title'] = song.get('title')
                track['artist'] = song.get('uploader')
                track['thumbnail'] = song.get('thumbnails', [{},])[-1].get('url', '')
                playlist['songs'].append(track)
            if update:
                self.LISTS.append(playlist)
                self.UPDATE_TITLE_LIST()
                sendUpdate()
                self.CHECK_TITLE_LIST(sendUpdate = sendUpdate)

        def PLAYLIST_INFO(self, id:str) -> dict:
            assert isinstance(id, str)
            for a in self.LISTS:
                if id == a['id']:
                    return a
            raise Exception('invalid/non-local playlist')

        def LIST_PLAYLISTS_INFO(self, GUI:bool = False) -> list:
            LISTS = self.LISTS
            if GUI:
                LISTS = []
                for playlist in self.LISTS:
                    id = playlist['id']
                    if not fd.isFile('youtube/%s.jpg' % id):
                        self.CHECK_TITLE_LIST()
                    else:
                        LISTS.append(playlist)
            return LISTS

        def DELETE_PLAYLIST(self, id:str) -> None:
            assert isinstance(id, str)
            for playlist in self.LISTS:
                if playlist['id'] == id:
                    self.LISTS.remove(playlist)
                    fd.deleteFile('youtube/%s.jpg' % playlist['id'])
                    self.UPDATE_TITLE_LIST()

    def PLAY_TRACK(PROVIDER:object, id:str):
        return Audio.Player(PROVIDER.DOWNLOAD_TRACK(id))
