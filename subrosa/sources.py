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
                }],
                'outtmpl': os.path.join(fd.directory, 'youtube/%(id)s.%(ext)s'),
                'quiet': True,
                'noplaylist': True,
                'writethumbnail': True,
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
                    with youtube_dl.YoutubeDL(opts) as ydl:
                        info = ydl.extract_info(url, download = True)
                        response['id'] = info.get('id')
                        response['title'] = info.get('title')
                        response['artist'] = info.get('uploader')
                        response['thumbnail'] = info.get('thumbnail')
                    if not response['thumbnail'].endswith('jpg'):
                        image = PIL.Image.open(os.path.join(fd.directory, 'youtube/%s.%s' % (response['id'], response['thumbnail'].split('.')[-1]))).convert('RGB')
                        image.save(os.path.join(fd.directory, 'youtube/%s.jpg' % response['id']), 'jpeg')
                        fd.deleteFile('youtube/%s.%s' % (response['id'], response['thumbnail'].split('.')[-1]))
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
        return Audio.Player(PROVIDER.DOWNLOAD_TRACK(id))
