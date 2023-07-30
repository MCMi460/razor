# MCMi460 on Github
from subrosa import *
from layout.mainwindow import Ui_MainWindow
from layout.credits import Ui_Credits
from layout.terms import Ui_Terms
from layout.miniplayer import Ui_Mini
from layout.settings import Ui_Settings
from layout.install import Ui_Install
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from notifypy import Notify

con = None

# Create GUI
class GUI(Ui_MainWindow):
    def __init__(self, MainWindow):
        global con
        self.MainWindow = MainWindow
        
        # Discord
        self.pid = os.getpid()
        self.party_id = random.getrandbits(128)

        # Triggers
        self.underLyingButton = QPushButton()
        self.underLyingButton.clicked.connect(lambda a : self.queueUpdate(True))
        self.triggerMain = QPushButton()
        self.triggerMain.clicked.connect(lambda a : self.fillMainWindow())

        # Abstract variables
        con = Console(sendUpdate = self.triggerMain.clicked.emit) # Begin main thread for user
        self.providerName = 'youtube'
        self.provider = con._getProvider(self.providerName)
        self.queue = []
        self.backQueue = []
        self.looping = False
        self.searching = False
        self.searchResults = []
        self.sliding = False
        self.downloading = []
        self.songSinceStartUp = 0

        self.cache = {
            'title': '',
            'artist': '',
            'thumbnail': '',
            'id': '',
        }

        # Events
        self.MainWindow.closeEvent = self.closeEvent

    def setup(self):
        # OS specifics #
        if sys.platform.startswith('darwin'): # Mac
            import AppKit
            NSApp = AppKit.NSApplication.sharedApplication()

            red = AppKit.NSColor.redColor()
            NSApp._setAccentColor_(red)

            accent = NSApp._accentColor()
            print(fd.log('[Accent (Mac)] %s' % accent))
            if not accent == red:
                print(fd.log('[Accent change failed!]'))
        elif os.name == 'nt': # Windows
            pass

        # Main Window
        self.MainWindow.setFixedSize(960, 600)
        self.MainWindow.setWindowIcon(QIcon(getPath('layout/resources/logo.ico')))

        # Top Menu
        self.topMenu.setCurrentIndex(0)

        # Queue Menu
        self.queueArea.hide()
        self.clearButton.hide()
        self.queueLayout = QGridLayout()
        self.queueContents.setLayout(self.queueLayout)
        self.queueUpdate()

        # Music Area
        self.musicLayout = QGridLayout()
        self.musicContents.setLayout(self.musicLayout)
        # Playlist Area
        self.playlistArea.hide()

        # Menu Bar
        self.menuBar.move(0, 0)
        self.menuBar.setFixedSize(960, 20)
        # Razor
        self.a_settings.triggered.connect(self.showSettings)
        self.a_credits.triggered.connect(self.showCredits)
        self.a_closeApp.triggered.connect(self.MainWindow.close)
        # File
        self.a_showSource.triggered.connect(lambda e : os.system('start %s' % appPath) if os.name == 'nt' else os.system('open %s' % appPath))
        self.a_newPlaylist.triggered.connect(lambda e : print('New Playlist!'))
        self.a_playlistYoutube.triggered.connect(lambda e : self.playlistYoutube())
        # Help
        self.a_issue.triggered.connect(lambda e : webbrowser.open('https://github.com/MCMi460/razor/issues/new'))

        # Volume
        self.volumeSlider.setValue(con.config['volume'])

        # Images
        icons = {
            'playImage': 'play.png',
            'pauseImage': 'pause.png',
            'loopImage': 'loop.png',
            'loopActivatedImage': 'loop2.png',
            'shuffleImage': 'shuffle.png',
            'backImage': 'rewind.png',
            'nextImage': 'skip.png',
            'modeImage': 'mode.png',
            'queueImage': 'queue.png',
            'searchImage': 'search.png',
            'homeImage': 'home.png',
            'picture': 'picture.png',
        }
        pixmaps = {
            'blankThumbnail': 'thumbnail.png',
            'audio1': 'audio1.png',
            'audio2': 'audio2.png',
        }
        self.lightImages = icons.copy() | pixmaps.copy()
        self.darkImages = icons.copy() | pixmaps.copy()
        for theme in ('light', 'dark'):
            # QSS Stylesheet (redundancy check?)
            with open(getPath('layout/resources/%s/styles.qss' % theme), 'r') as file:
                getattr(self, theme + 'Images')['qss'] = file.read()
            for key in list(icons.keys()):
                getattr(self, theme + 'Images')[key] = QIcon(getPath(('layout/resources/%s/' % theme) + icons[key]))
            for key in list(pixmaps.keys()):
                getattr(self, theme + 'Images')[key] = QPixmap(getPath(('layout/resources/%s/' % theme) + pixmaps[key]))

        if con.config['darkMode']:
            self.theme = self.darkImages
        else:
            self.theme = self.lightImages

        self.movie = QMovie(getPath('layout/resources/loading.gif'))
        self.loadingGif.setMovie(self.movie)
        self.loadingGif.setScaledContents(True)

        # Connections
        self.playButton.clicked.connect(self.toggle)
        self.forwardButton.clicked.connect(lambda event : self.next())
        self.backButton.clicked.connect(self.back)
        self.loopButton.clicked.connect(self.loop)
        self.themeButton.clicked.connect(self.toggleTheme)
        self.volumeMax.mouseReleaseEvent = lambda a : self.volumeSlider.setValue(self.volumeSlider.value() + 20)
        self.volumeMin.mouseReleaseEvent = lambda a : self.volumeSlider.setValue(self.volumeSlider.value() - 20)
        self.queueButton.clicked.connect(self.toggleQueue)
        self.clearButton.clicked.connect(self.clearQueue)
        self.shuffleButton.clicked.connect(self.shuffle)
        self.searchButton.clicked.connect(self.toggleSearch)

        self.progressBar.sliderPressed.connect(self.pauseProgress)
        self.progressBar.sliderReleased.connect(self.updateDuration)
        self.progressBar.mouseReleaseEvent = self.updatePosition
        self.volumeSlider.valueChanged.connect(self.updateVolume)

        self.searchBar.returnPressed.connect(self.searchFinish)

        self.themeUpdate()
        self.fillMainWindow()
        self.updateFont()

        pre = con.config['acceptedTerms;%s' % version]
        self.terms()

        self.installs(pre)

    def miniplayer(self):
        window = MiniPlayer(self)
        window.window.setStyleSheet(self.theme['qss'])
        window.window.exec_()

    def terms(self):
        if not con.config['acceptedTerms;%s' % version]:
            window = Terms()
            window.dialog.setStyleSheet(self.theme['qss'])
            window.dialog.exec_()

    def installs(self, pre):
        if not pre:
            window = Install()
            window.dialog.setStyleSheet(self.theme['qss'])
            window.firstLaunchSetup()
            window.dialog.exec_()

    def toggle(self):
        if con.track['media'] and con.track['media'].is_playing():
            self.pause()
            self.playButton.setIcon(self.theme['playImage'])
        else:
            self.play()

    def play(self, id = None):
        if con.track['media'] and con.track['media'].get_state() == Audio.State.Paused:
            self.resume()
        elif con.track == track:
            self.songSinceStartUp += 1
            con.track['provider'] = True
            if len(self.queue) == 0:
                try:
                    self.addToQueue(id)
                except:
                    con.track['provider'] = None
                    return
            if not id:
                id = self.queue[0]
            threading.Thread(target = self._constantPlay, args = (self.providerName, id,), daemon = True).start()
        self.playButton.setIcon(self.theme['pauseImage'])
        self.underLyingButton.clicked.emit()

    def _constantPlay(self, provider, id):
        #while id in self.downloading:
        #    pass
        self.downloading.append(id)
        con.play(provider, id, False)
        self.downloading.remove(id)
        self.triggerMain.clicked.emit()
        con.track['media'].set_volume(self.volumeSlider.value())
        while con.track['media'] and not con.track['media'].is_playing():
            pass
        self.party_id = random.getrandbits(128)
        threading.Thread(target = self.updateMeta, args = (id,), daemon = True).start()
        self.progressBar.setValue(0)
        length = con.track['media'].get_length()
        self.progressBar.setMaximum(length)
        self.sliding = False
        self.endTime.setText(self.convertToTimestamp(length))
        threading.Thread(target = self.updateProgressBar, daemon = True).start()
        self.playButton.setIcon(self.theme['pauseImage'])
        while con.track['media'] and con.track['media'].get_state() in (Audio.State.Playing, Audio.State.Paused):
            pass
        if con.track['media']:
            self.next()
        else:
            self.stop()

    def next(self, distance = 1, clicked = False):
        if con.track['media']:
            self.stop()
        if not self.looping or clicked:
            for i in range(distance):
                if len(self.queue) > 0:
                    self.backQueue.append(self.queue.pop(0))
            if len(self.queue) > 0:
                self.play(self.queue[0])
        else:
            if len(self.queue) > 0:
                self.play(self.queue[0])
        self.underLyingButton.clicked.emit()

    def back(self):
        if con.track['media'] and ( (con.track['media'].get_time() > 2000 and con.track['media'].get_length() > 3000) ):
            con.track['media'].set_time(0)
            self.queueUpdate(True)
            return
        elif con.track['media']:
            self.stop()
            self.queueUpdate()
        if len(self.backQueue) > 0:
            self.queue.insert(0, self.backQueue.pop(-1))
            if len(self.queue) > 0:
                self.play(self.queue[0])
            self.queueUpdate(True)

    def addToQueue(self, id:str, pos:int = None):
        if not id:
            tracks = self.provider.LIST_TRACKS(GUI = True)
            if len(tracks) == 0:
                raise Exception('no songs!')
            id = random.choice(self.provider.LIST_TRACKS(GUI = True))
        if not pos:
            self.queue.append(id)
        else:
            self.queue.insert(pos, id)
        self.queueUpdate()
        return pos if len(self.queue) > 1 else 0

    def stop(self, closing = False):
        try:
            con.stop()
        except:
            pass
        if not closing:
            self.progressBar.setValue(0)
            self.currentTime.setText('0:00')
            self.endTime.setText('0:00')
            self.playButton.setIcon(self.theme['playImage'])
            self.updateMeta()

    def pause(self):
        con.pause()

    def resume(self):
        con.resume()

    def loop(self):
        self.looping = not self.looping
        key = 'loopImage'
        if self.looping:
            key = 'loopActivatedImage'
        self.loopButton.setIcon(self.theme[key])

    def cooldown(self, element, sec:int):
        def wait():
            element.setEnabled(False)
            time.sleep(sec)
            element.setEnabled(True)
        threading.Thread(target = wait, daemon = True).start()

    def playlistYoutube(self):
        link, ok = QInputDialog.getText(self.MainWindow, 'New Youtube Playlist', 'Enter the link of your Youtube playlist (must be public/unlisted):')
        if not ok:
            return
        else:
            try:
                url = urllib.parse.urlparse(link)
                if not url.netloc in ('www.youtube.com', 'youtube.com') or not url.path == '/playlist':
                    raise Exception('That is an invalid Youtube playlist link.')
                id = urllib.parse.parse_qs(url.query)['list'][0]
                self.provider.ADD_PLAYLIST(id, sendUpdate = self.triggerMain.clicked.emit)
            except Exception as e:
                self.errorDialog(str(e))

    def updateMeta(self, id:str = None):
        if not id:
            info = {
                'title': '',
                'artist': '',
                'thumbnail': '',
                'id': '',
            }
        else:
            info = self.provider.TRACK_INFO(con.track['id'])
        metric = self.titleLabel.fontMetrics()
        self.titleLabel.setText(metric.elidedText(info['title'], Qt.ElideRight, 380))
        self.uploaderLabel.setText(info['artist'])
        if not id:
            pix = self.theme['blankThumbnail']
        else:
            pix = QPixmap(os.path.abspath(os.path.join(fd.directory, '%s/%s.jpg' % (self.providerName, id))))
        self.cache = info.copy()
        self.thumbnailLabel.setPixmap(pix)

    # Discord RPC
    def connect(self):
        global connected, rpc
        try:
            rpc = pypresence.Client('874365581162328115', pipe = 0) # Razor's Discord Application ID
        except Exception as e:
            print(fd.log('[Cannot initialize RPC: %s]' % e))
            connected = False
            return
        try:
            rpc.start()
            connected = True
            print(fd.log('[Successful connection to Discord]'))
            rpc.clear_activity(pid = os.getpid())
        except Exception as e:
            print(fd.log('[Failed connection to Discord]'))
            print(fd.log('[Cannot connect RPC: %s]' % e))
            connected = False

    def join(self, ev):
        print(ev)
        secret = ev['secret'].split(' ')
        # self.party_id = secret[1]
        # This doesn't do anything for now.
        self.stop()
        self.play(secret[0])
    
    def join_request(self, ev):
        print(ev)
        notification = Notify()
        notification.title = '%s wants to listen to your song!' % ev['user']['global_name']
        notification.message = 'See Discord to accept!'
        #notification.icon = 'https://cdn.discordapp.com/avatars/%s/%s.png' % (ev['user']['id'], ev['user']['avatar']) # (or .gif)
        
        notification.send()
    
    def events(self):
        rpc.register_event('ACTIVITY_JOIN', self.join)
        rpc.register_event('ACTIVITY_JOIN_REQUEST', self.join_request)
        rpc.subscribe('ACTIVITY_JOIN')
        rpc.subscribe('ACTIVITY_JOIN_REQUEST')
        #if 'join' in sys.argv:
            #rpc.read()

    def updatePresence(self, info:dict = {}):
        for key in info.keys():
            self.cache[key] = info[key]
        dict = {
            'details': self.cache['title'],
            'large_image': self.cache['thumbnail'],
            'large_text': self.cache['title'],
            #'buttons': [{'label': 'YouTube', 'url':'https://youtube.com/watch?v=%s' % self.cache['id']}],
            'small_image': 'logo',
            'small_text': 'Razor v%s' % version,
            'join': self.cache['id'] + ' ' + str(self.party_id),
            'party_size': [1, 2],
            'party_id': str(self.party_id),
        }
        try:
            if con.track['media'] and con.track['media'].is_playing():
                dict['end'] = time.time() + (con.track['media'].get_length() - con.track['media'].get_time()) / 1000
        except:
            pass
        try:
            if con.track['media'] and con.track['media'].is_paused():
                dict['state'] = 'Paused'
        except:
            pass
        try:
            print(fd.log('[Discord request]'))
            if not self.cache['title']:
                rpc.clear_activity(pid = self.pid)
            else:
                rpc.set_activity(pid = self.pid, **dict)
        except pypresence.exceptions.PipeClosed:
            print(fd.log('[Discord pipe closed. Attempting reconnect]'))
            connect()
        except RuntimeError as e:
            print(fd.log('[Discord event loop error ignored: %s]' % e))

    def _constantDiscord(self):
        while connected:
            self.updatePresence()
            time.sleep(2)

    def loadPlaylistMeta(self, playlist):
        playlist = self.provider.PLAYLIST_INFO(playlist)
        # Put actual code
        # here
        self.playlistArea.show()
        self.searchButton.setIcon(self.theme['homeImage'])
        self.toggleQueue(None, True)

    def updateProgressBar(self):
        num = self.songSinceStartUp
        while con.track['media'] and con.track['media'].get_state() in (Audio.State.Playing, Audio.State.Paused):
            if num != self.songSinceStartUp:
                break
            currentDuration = con.track['media'].get_time()
            if not self.sliding:
                self.progressBar.setValue(currentDuration)
            self.currentTime.setText(self.convertToTimestamp(currentDuration))
            time.sleep(0.1)

    def updateDuration(self):
        if con.track['media']:
            con.track['media'].set_time(self.progressBar.value())
        else:
            self.stop()
        self.sliding = False

    def updatePosition(self, event):
        if con.track['media'] and not con.track['media'].get_state() == Audio.State.Stopped and not self.progressBar.isSliderDown():
            duration = QStyle.sliderValueFromPosition(self.progressBar.minimum(), self.progressBar.maximum(), event.y(), self.progressBar.height())
            con.track['media'].set_time(duration)
            self.currentTime.setText(self.convertToTimestamp(duration))
            self.progressBar.setValue(duration)
        self.progressBar.setSliderDown(False)

    def toggleTheme(self):
        if self.theme == self.lightImages:
            self.theme = self.darkImages
            con.config['darkMode'] = True
        else:
            self.theme = self.lightImages
            con.config['darkMode'] = False

        con._updateConfig()
        self.themeUpdate()

    def themeUpdate(self):
        ### STYLESHEET START ###

        self.MainWindow.setStyleSheet(self.theme['qss'])

        # Label images
        if con.track['media'] and con.track['media'].is_playing():
            self.playButton.setIcon(self.theme['pauseImage'])
        else:
            self.playButton.setIcon(self.theme['playImage'])
        self.playButton.setIconSize(self.playButton.size())

        self.backButton.setIcon(self.theme['backImage'])
        self.backButton.setIconSize(self.backButton.size())
        self.forwardButton.setIcon(self.theme['nextImage'])
        self.forwardButton.setIconSize(self.forwardButton.size())

        key = 'loopImage'
        if self.looping:
            key = 'loopActivatedImage'
        self.loopButton.setIcon(self.theme[key])
        self.loopButton.setIconSize(self.loopButton.size())
        self.shuffleButton.setIcon(self.theme['shuffleImage'])
        self.shuffleButton.setIconSize(self.shuffleButton.size())

        self.queueButton.setIcon(self.theme['queueImage'])
        self.queueButton.setIconSize(self.queueButton.size())

        self.volumeMin.setPixmap(self.theme['audio1'])
        self.volumeMin.setScaledContents(True)
        self.volumeMax.setPixmap(self.theme['audio2'])
        self.volumeMax.setScaledContents(True)

        self.themeButton.setIcon(self.theme['modeImage'])
        self.themeButton.setIconSize(self.themeButton.size())
        if self.topMenu.currentIndex() == 0:
            self.searchButton.setIcon(self.theme['searchImage'])
        else:
            self.searchButton.setIcon(self.theme['homeImage'])
        self.searchButton.setIconSize(self.searchButton.size())

        self.thumbnailLabel.setScaledContents(True)

        if not con.track['media']:
            self.updateMeta()

        ### STYLESHEET END ###

    def updateVolume(self):
        vol = self.volumeSlider.value()
        if con.track['media']:
            con.track['media'].set_volume(vol)
        con.config['volume'] = vol
        con._updateConfig()

    def pauseProgress(self):
        if con.track['media']:
            self.sliding = True

    def emptyLayout(self, layout):
        if layout:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget != None:
                    widget.deleteLater()
                else:
                    self.emptyLayout(item.layout())

    def queueUpdate(self, forceStart = False):
        self.emptyLayout(self.queueLayout)
        y = 0
        if len(self.queue) > 1 or (not con.track['media'] and len(self.queue) > 0):
            start = 1
            if not con.track['media'] and not forceStart:
                start = 0
            for i in range(start, len(self.queue)):
                if i > 6:
                    break
                group = QGroupBox()
                group.move(0, y)
                group.setFixedSize(119, 71)
                label = QLabel(group)
                label.move(5,5)
                label.resize(109, 61)
                pix = QPixmap(os.path.abspath(os.path.join(fd.directory, '%s/%s.jpg' % (self.providerName, self.queue[i]))))
                label.setPixmap(pix)
                label.setScaledContents(True)
                label.mouseReleaseEvent = lambda event, i = i : self.next(i, True) if event.button() == Qt.LeftButton else None
                label.contextMenuEvent = lambda event, i = i : self.queueSongDropdown(event, i)
                label.setCursor(QCursor(Qt.PointingHandCursor))
                self.queueLayout.addWidget(group)
                y += 80
        # Fun little message
        endg = QGroupBox()
        endg.setStyleSheet('background-color: transparent;')
        endg.move(0, y)
        endg.setFixedSize(119, 100)
        end = QLabel(endg)
        end.setText('There\'s more here, but it\'s too big to show!' if len(self.queue) > 7 else 'You\'ve reached the end!')
        end.resize(109, 90)
        end.setWordWrap(True)
        end.setAlignment(Qt.AlignCenter)
        self.queueLayout.addWidget(endg)
        # Spacer
        self.queueLayout.addItem(QSpacerItem(0, 471))

    def toggleQueue(self, event, hide = False):
        #self.miniplayer()
        if self.queueArea.isVisible() or hide:
            self.queueArea.hide()
            self.clearButton.hide()
        else:
            self.queueArea.show()
            self.clearButton.show()

    def shuffle(self):
        if len(self.queue) > 1:
            list = self.queue[1:]
            random.shuffle(list)
            for i in range(1, len(self.queue)):
                self.queue[i] = list[i - 1]
            self.queueUpdate()

    def fillMainWindow(self):
        if self.topMenu.currentIndex() == 0:
            songs = self.provider.LIST_TRACKS_INFO(GUI = True)
            playlists = self.provider.LIST_PLAYLISTS_INFO(GUI = True)
            menu = False
        else:
            songs = self.searchResults
            playlists = []
            menu = True
        self.emptyLayout(self.musicLayout)
        y, rows = 0, 0
        if len(playlists) > 0:
            self.addEntry('Playlists', y, align = Qt.AlignLeft, header = True)
            y, rows = self.addEntries(playlists, menu = menu)
            self.addEntry('Songs', y, align = Qt.AlignLeft, header = True)
        y_, rows_ = self.addEntries(songs, menu = menu)
        y += y_
        rows += rows_
        if menu and rows == 0:
            self.addEntry('Searching for music online may take some time. Please be patient.', y)
        if rows <= 4:
            self.musicLayout.addItem(QSpacerItem(0, 107 * (5 - rows) + 15 * (5 - rows) - 50))
        self.addEntry('You\'ve reached the end!', y)

    def addEntries(self, songs:list, *, menu = False):
        y = 16
        rows = math.ceil(len(songs) / 4)
        for row in range(rows):
            overlay = QGroupBox()
            overlay.setStyleSheet('background-color: transparent;')
            overlay.move(16, y)
            overlay.setFixedSize(809, 107)
            for i in range(4):
                n = 4 * row + i
                if n > len(songs) - 1:
                    break
                thumbnail = QLabel(overlay)
                thumbnail.move(i * 191 + 15 * i, 0)
                thumbnail.setFixedSize(191, 107)
                thumbnail.setScaledContents(True)
                if songs[n].get('online'):
                    pix = QPixmap()
                    pix.loadFromData(requests.get(songs[n]['thumbnail'], verify = False).content)
                else:
                    pix = QPixmap(os.path.abspath(os.path.join(fd.directory, '%s/%s.jpg' % (self.providerName, songs[n]['id']))))
                thumbnail.setPixmap(pix)
                overPicture = QGroupBox(overlay)
                overPicture.move(i * 191 + 15 * i, 0)
                overPicture.setFixedSize(191, 107)
                overPicture.setStyleSheet('')
                if songs[n].get('playlist'):
                    overPicture.mouseReleaseEvent = lambda event, n = songs[n] : self.loadPlaylistMeta(n['id'])
                else:
                    overPicture.mouseReleaseEvent = lambda event, n = songs[n] : self.next(self.addToQueue(n['id'], 1), True) if event.button() == Qt.LeftButton else None
                if not menu:
                    if songs[n].get('playlist'):
                        overPicture.contextMenuEvent = lambda event, id = songs[n]['id'] : self.playlistDropdown(event, id)
                    else:
                        overPicture.contextMenuEvent = lambda event, id = songs[n]['id'] : self.downloadedSongDropdown(event, id)
                else:
                    overPicture.contextMenuEvent = lambda event, id = songs[n]['id'] : self.onlineSongsDropdown(event, id)
                title = QLabel(overPicture)
                title.setFixedSize(181, 65)
                title.move(5,5)
                title.setText(songs[n]['title'])
                self.resizeFontHeight(title)
                style = 'background-color:transparent; color: #FFF;'
                title.setStyleSheet(style)
                title.setWordWrap(True)
                title.setAlignment(Qt.AlignCenter)
                title.hide()
                artist = QLabel(overPicture)
                artist.setFixedSize(181, 30)
                artist.move(5, 65)
                artist.setText(songs[n]['artist'])
                artist.setStyleSheet(style)
                artist.setWordWrap(True)
                artist.setAlignment(Qt.AlignCenter)
                artist.hide()
                def show(overPicture, title, artist):
                    overPicture.setStyleSheet('background-color:rgba(0,0,0,0.5);')
                    title.show()
                    artist.show()
                def hide(overPicture, title, artist):
                    overPicture.setStyleSheet('')
                    title.hide()
                    artist.hide()
                overPicture.enterEvent = lambda e, overPicture = overPicture, title = title, artist = artist : show(overPicture, title, artist)
                overPicture.leaveEvent = lambda e, overPicture = overPicture, title = title, artist = artist : hide(overPicture, title, artist)
                overPicture.setCursor(QCursor(Qt.PointingHandCursor))
            self.musicLayout.addWidget(overlay)
            y += 122
        return y, rows

    def addEntry(self, text, y, *, align = Qt.AlignCenter, header = False):
        endg = QGroupBox()
        endg.setStyleSheet('background-color: transparent;')
        endg.move(0, y)
        endg.setFixedSize(809, 50)
        end = QLabel(endg)
        end.setText(text)
        end.resize(799, 50)
        if header:
            self.resizeFontWidth(end)
        end.setWordWrap(True)
        end.setAlignment(align)
        self.musicLayout.addWidget(endg)

    def downloadedSongDropdown(self, event, id:str):
        contextMenu = QMenu(self.MainWindow)
        play = contextMenu.addAction('Play')
        add = contextMenu.addAction('Add to queue')
        delete = contextMenu.addAction('Delete')
        action = contextMenu.exec_(event.globalPos())
        if action == add:
            self.addToQueue(id)
        elif action == play:
            self.next(self.addToQueue(id, 1), True)
        elif action == delete:
            if len(self.queue) > 0:
                if id == self.queue[0]:
                    self.stop()
            self.provider.DELETE_TRACK(id)
            for i in range(self.queue.count(id)):
                self.queue.remove(id)
            for i in range(self.backQueue.count(id)):
                self.backQueue.remove(id)
            self.fillMainWindow()
            self.queueUpdate()

    def queueSongDropdown(self, event, position:int):
        contextMenu = QMenu(self.MainWindow)
        skip = contextMenu.addAction('Skip to here')
        remove = contextMenu.addAction('Remove from queue')
        action = contextMenu.exec_(event.globalPos())
        if action == skip:
            self.next(position, True)
        elif action == remove:
            self.queue.pop(position)
            self.queueUpdate()

    def onlineSongsDropdown(self, event, id:str):
        contextMenu = QMenu(self.MainWindow)
        play = contextMenu.addAction('Play')
        download = contextMenu.addAction('Download')
        action = contextMenu.exec_(event.globalPos())
        if action == play:
            self.next(self.addToQueue(id, 1), True)
        elif action == download:
            def download():
                #while id in self.downloading:
                #    pass
                self.downloading.append(id)
                self.provider.DOWNLOAD_TRACK(id)
                self.downloading.remove(id)
                self.triggerMain.clicked.emit()
            threading.Thread(target = download, daemon = True).start()

    def playlistDropdown(self, event, id:str):
        contextMenu = QMenu(self.MainWindow)
        open = contextMenu.addAction('Open')
        delete = contextMenu.addAction('Delete')
        action = contextMenu.exec_(event.globalPos())
        if action == open:
            self.loadPlaylistMeta(id)
        elif action == delete:
            self.provider.DELETE_PLAYLIST(id)
            self.fillMainWindow()

    def toggleSearch(self):
        if self.playlistArea.isVisible():
            self.playlistArea.hide()
            self.searchButton.setIcon(self.theme['searchImage'])
            self.toggleQueue(None, True)
            self.fillMainWindow()
        else:
            if self.topMenu.currentIndex() == 0:
                self.searchButton.setIcon(self.theme['homeImage'])
                self.topMenu.setCurrentIndex(1)
                self.toggleQueue(None, True)
                self.fillMainWindow()
            else:
                self.searchButton.setIcon(self.theme['searchImage'])
                self.topMenu.setCurrentIndex(0)
                self.toggleQueue(None, True)
                self.fillMainWindow()

    def searchFinish(self):
        if not self.searching:
            self.searching = True
            self.searchBar.setEnabled(False)
            self.loadingGif.show()
            self.movie.start()
            threading.Thread(target = self.processSearch, daemon = True).start()

    def processSearch(self):
        terms = self.searchBar.text()
        if not terms:
            self.searchResults = []
        else:
            url = urllib.parse.urlparse(terms)
            if url.scheme and url.netloc in ('www.youtube.com', 'youtube.com'):
                id = urllib.parse.parse_qs(url.query)['v'][0]
                searchResults = [self.provider.TRACK_INFO(id),]
            elif url.scheme and url.netloc in ('www.youtu.be', 'youtu.be'):
                id = url.path.replace('/', '')
                searchResults = [self.provider.TRACK_INFO(id),]
            else:
                searchResults = self.provider.SEARCH(terms)
            self.searchResults = []
            for result in searchResults:
                if not 'Music' in result.get('categories', []) and not terms.startswith('http'):
                    continue
                final = {}
                final['id'] = result.get('id')
                final['title'] = result.get('title')
                final['artist'] = result.get('uploader')
                final['thumbnail'] = result.get('thumbnail')
                final['online'] = True
                final['playlist'] = False
                self.searchResults.append(final)
        self.triggerMain.clicked.emit()
        self.searchBar.setEnabled(True)
        self.loadingGif.hide()
        self.movie.stop()
        self.searching = False

    def clearQueue(self):
        start = 1
        if not con.track['media']:
            start = 0
        for song in self.queue[start:]:
            self.queue.remove(song)
        self.queueUpdate()

    def showCredits(self):
        window = Credits()
        window.dialog.setStyleSheet(self.darkImages['qss'])
        window.dialog.exec_()

    def showSettings(self):
        window = Settings(self)
        window.dialog.setStyleSheet(self.theme['qss'])
        window.dialog.exec_()

    def updateFont(self):
        font = QFont('Arial', (10 if os.name == 'nt' else 13) + con.config['fontOffset'])
        app.setFont(font, 'QLabel')
        app.setFont(font, 'QPushButton')

    def resizeFontWidth(self, label):
        i = 40
        width = label.width() + 1
        while label.width() < width:
            i -= 1
            label.setFont(QFont('Arial', i))
            width = label.fontMetrics().width(label.text())

    def resizeFontHeight(self, label):
        i = 30
        height = label.fontMetrics().height() # This does not get height post-word-wrap

    def closeEvent(self, event):
        self.stop(True)
        try:
            rpc.close()
        except:
            pass
        event.accept()
        sys.exit()

    def convertToTimestamp(self, milliseconds:int):
        min, sec = divmod(milliseconds / 1000, 60)
        return '%s:%s' % (int(min), str(int(sec)).zfill(2))

    def errorDialog(self, text:str):
        dialog = QMessageBox(
            text = text,
            parent = self.MainWindow,
        )
        dialog.exec_()

class Credits(Ui_Credits):
    def __init__(self):
        self.dialog = QDialog()
        self.setupUi(self.dialog)

        self.dialog.setFixedSize(600, 400)

        self.imageLabel.setPixmap(QPixmap(getPath(('layout/resources/emblem.png'))))
        self.imageLabel.setScaledContents(True)

        self.versionLabel.setText('Razor v%s' % version)

        self.gitLink.mouseReleaseEvent = lambda e : self.openLink('https://github.com/MCMi460/razor')

        self.mrgamedood.mouseReleaseEvent = lambda e : self.openLink('https://github.com/mrgamecub3')
        self.deltaboi.mouseReleaseEvent = lambda e : self.openLink('https://github.com/MCMi460')

    def openLink(self, url:str):
        webbrowser.open(url)

class Terms(Ui_Terms):
    def __init__(self):
        self.dialog = QDialog()
        self.setupUi(self.dialog)

        self.dialog.setFixedSize(600, 400)

        self.versionLabel.setText('Razor v%s Terms Document' % version)

        self.declineButton.clicked.connect(self.dialog.close)
        self.acceptButton.clicked.connect(self.accept)

        self.dialog.closeEvent = self.closeEvent

    def accept(self):
        con.config['acceptedTerms;%s' % version] = True
        con._updateConfig()
        self.dialog.close()

    def closeEvent(self, event):
        event.accept()
        if not con.config['acceptedTerms;%s' % version]:
            sys.exit()

class Install(Ui_Install):
    def __init__(self):
        self.dialog = QDialog()
        self.setupUi(self.dialog)

        self.dialog.setFixedSize(600, 400)

        self.dialog.closeEvent = self.closeEvent

        self.done = False

        # Remove:
        #os.name = 'nt'

        # Buttons
        self.quit1.clicked.connect(lambda a : self.close())
        self.next1.clicked.connect(lambda a : self.ffmpegInstallSetup())
        if os.name == 'nt':
            self.windowsBox.setEnabled(True)
        elif sys.platform.startswith('darwin'):
            self.macBox.setEnabled(True)
        self.next2.clicked.connect(lambda a : self.installingSetup())
        self.back2.clicked.connect(lambda a : self.firstLaunchSetup())
        self.quit2.clicked.connect(lambda a : self.close())
        self.next3.clicked.connect(lambda a : self.close(True))
        self.quit3.clicked.connect(lambda a : self.close())

        self.installText = ''
        self.triggerHook = QPushButton()
        self.triggerHook.clicked.connect(lambda a : self.installProgress.setPlainText(self.installText))

    def firstLaunchSetup(self):
        self.pages.setCurrentIndex(0)

        # Labels
        self.razorLogo.setPixmap(QPixmap(getPath('layout/resources/logo.png')))
        self.phaseLabel.setText('Setup Menu')
        GUI.resizeFontWidth(self, self.phaseLabel)

    def ffmpegInstallSetup(self):
        self.pages.setCurrentIndex(1)

        # Labels
        self.phaseLabel.setText('FFMPEG Install')
        GUI.resizeFontWidth(self, self.phaseLabel)
        if os.name == 'nt':
            self.linkEdit2.setVisible(False)
            self.linkEdit.setText('https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip')
        else:
            self.linkEdit.setText('https://evermeet.cx/ffmpeg/getrelease/ffprobe/zip')
            self.linkEdit2.setText('https://evermeet.cx/ffmpeg/getrelease/zip')

    def installingSetup(self):
        self.pages.setCurrentIndex(2)
        self.next3.setVisible(False)
        self.quit3.setVisible(False)

        if not os.path.exists(con.config['ffmpeg']):
            self.hook('[No FFMPEG detected!]')
            # Ensue installing FFMPEG via window
            # For now, we do it automatically
            from scripts.ffmpeg import installFFMPEG, installFFMPEGMac
            threading.Thread(
                target = installFFMPEG if os.name == 'nt' else installFFMPEGMac,
                args = (
                    con.config['ffmpeg'],
                    os.path.abspath(appPath),
                    self.linkEdit.text() if os.name == 'nt' else [self.linkEdit.text(),self.linkEdit2.text()],
                ),
                kwargs = {
                    'hook': self.hook,
                },
                daemon = True,
            ).start()
        else:
            self.hook('[FFMPEG found! Skipping install.]', True)

    def hook(self, text, finished = False):
        self.installText += text + '\n'
        self.triggerHook.clicked.emit()
        if finished:
            if finished == 'Fail':
                self.quit3.setVisible(True)
            else:
                self.next3.setVisible(True)

    def close(self, done:bool = False):
        self.done = done
        self.dialog.close()

    def closeEvent(self, event):
        event.accept()
        if not self.done:
            con.config['acceptedTerms;%s' % version] = False
            con._updateConfig()
            sys.exit()

class MiniPlayer(Ui_Mini):
    def __init__(self, parent):
        self.parent = parent

        self.window = QDialog()
        self.setupUi(self.window)

        self.window.setFixedSize(427, 240)

class Settings(Ui_Settings):
    def __init__(self, parent):
        self.parent = parent

        self.dialog = QDialog()
        self.setupUi(self.dialog)

        self.dialog.setFixedSize(600, 400)

        self.fontSize.setValue(con.config['fontOffset'] + 13)

        self.fontSize.valueChanged.connect(self.update)

    def update(self):
        # Save values
        con.config['fontOffset'] = self.fontSize.value() - 13
        con._updateConfig()

        # Runtime changes
        self.parent.updateFont()

if __name__ == '__main__':
    # Main Window
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    MainWindow = QMainWindow()
    window = GUI(MainWindow)

    window.setupUi(MainWindow)
    window.setup()
    
    # Discord RPC
    connected = False
    rpc = None
    window.connect()
    if connected:
        window.events()
        threading.Thread(
            target = window._constantDiscord,
            args = (),
            daemon = True,
        ).start()

    MainWindow.show()

    app.exec_()
    mix.Mix_Quit()
    sys.exit()
