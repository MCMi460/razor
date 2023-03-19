# MCMi460 on Github
from subrosa import *
from layout import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

con = None

# Create GUI
class GUI(Ui_MainWindow):
    def __init__(self, MainWindow):
        global con
        self.MainWindow = MainWindow

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

        self.cache = {
            'title': '',
            'artist': '',
            'thumbnail': '',
            'id': '',
        }

        # Events
        # none thus far

    def setup(self):
        # Main Window
        self.MainWindow.setFixedSize(960, 600)

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
        self.end = QLabel()

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
        }
        pixmaps = {
            'blankThumbnail': 'thumbnail.png',
            'audio1': 'audio1.png',
            'audio2': 'audio2.png',
        }
        self.lightImages = icons.copy() | pixmaps.copy()
        self.darkImages = icons.copy() | pixmaps.copy()
        for type in ('light', 'dark'):
            # QSS Stylesheet (redundancy check?)
            with open('layout/resources/%s/styles.qss' % type, 'r') as file:
                getattr(self, type + 'Images')['qss'] = file.read()
            for key in list(icons.keys()):
                getattr(self, type + 'Images')[key] = QIcon(('layout/resources/%s/' % type) + icons[key])
            for key in list(pixmaps.keys()):
                getattr(self, type + 'Images')[key] = QPixmap(('layout/resources/%s/' % type) + pixmaps[key])

        self.theme = self.darkImages

        self.movie = QMovie('layout/resources/loading.gif')
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

        self.progressBar.sliderReleased.connect(self.updateDuration)
        self.volumeSlider.valueChanged.connect(self.updateVolume)

        self.searchBar.returnPressed.connect(self.searchFinish)

        self.themeUpdate()
        self.fillMainWindow()

    def toggle(self):
        if con.track['media'] and con.track['media'].is_playing():
            self.pause()
            self.playButton.setIcon(self.theme['playImage'])
        else:
            self.play()

    def play(self, id = None):
        if con.track['media'] and con.track['media'].get_state() == vlc.State.Paused:
            self.resume()
        elif con.track == track:
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
        con.play(provider, id, False)
        con.track['media'].audio_set_volume(self.volumeSlider.value())
        while con.track['media'] and not con.track['media'].is_playing():
            pass
        threading.Thread(target = self.updateMeta, args = (id,), daemon = True).start()
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(con.track['media'].get_length())
        threading.Thread(target = self.updateProgressBar, daemon = True).start()
        self.playButton.setIcon(self.theme['pauseImage'])
        while con.track['media'] and con.track['media'].get_state() in (vlc.State.Playing, vlc.State.Paused):
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
            tracks = self.provider.LIST_TRACKS()
            if len(tracks) == 0:
                raise Exception('no songs!')
            id = random.choice(self.provider.LIST_TRACKS())
        if not pos:
            self.queue.append(id)
        else:
            self.queue.insert(pos, id)
        self.queueUpdate()
        return pos if len(self.queue) > 1 else 0

    def stop(self):
        try:
            con.stop()
        except:
            pass
        self.progressBar.setValue(0)
        self.playButton.setIcon(self.theme['playImage'])
        self.updateMeta()

    def pause(self):
        con.pause()
        self.updatePresence()

    def resume(self):
        con.resume()
        self.updatePresence()

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
        self.titleLabel.setText(info['title'])
        self.uploaderLabel.setText(info['artist'])
        if not id:
            if connected and self.provider.setupFinish: rpc.clear()
            pix = self.theme['blankThumbnail']
        else:
            self.updatePresence(info)
            pix = QPixmap('sources/%s/%s.jpg' % (self.providerName, id))
        self.thumbnailLabel.setPixmap(pix)

    def updatePresence(self, info:dict = {}):
        for key in info.keys():
            self.cache[key] = info[key]
        dict = {
            'state': self.cache['title'],
            'large_image': self.cache['thumbnail'],
            'large_text': self.cache['title'],
            'buttons': [{'label': 'YouTube', 'url':'https://youtube.com/watch?v=%s' % self.cache['id']}],
            'small_image': 'logo',
            'small_text': 'Razor v%s' % version,
        }
        try:
            if con.track['media'] and con.track['media'].is_playing():
                dict['end'] = time.time() + (con.track['media'].get_length() - con.track['media'].get_time()) / 1000
        except:
            pass
        if not self.cache['title']:
            if connected and self.provider.setupFinish: rpc.clear()
        else:
            if connected and self.provider.setupFinish: rpc.update(**dict)

    def updateProgressBar(self):
        while con.track['media'] and con.track['media'].get_state() in (vlc.State.Playing, vlc.State.Paused):
            self.progressBar.setValue(con.track['media'].get_time())
            time.sleep(1)

    def updateDuration(self):
        if con.track['media']:
            con.track['media'].set_time(self.progressBar.value())
            self.updatePresence()
        else:
            self.stop()

    def toggleTheme(self):
        if self.theme == self.lightImages:
            self.theme = self.darkImages
        else:
            self.theme = self.lightImages

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
        if con.track['media']:
            con.track['media'].audio_set_volume(self.volumeSlider.value())

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
                group = QGroupBox()
                group.move(0, y)
                group.setFixedSize(119, 71)
                label = QLabel(group)
                label.move(5,5)
                label.resize(109, 61)
                pix = QPixmap('sources/%s/%s.jpg' % (self.providerName, self.queue[i]))
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
        endg.setFixedSize(119, 50)
        end = QLabel(endg)
        end.setText('You\'ve reached the end!')
        end.resize(109, 40)
        end.setWordWrap(True)
        end.setAlignment(Qt.AlignCenter)
        self.queueLayout.addWidget(endg)
        # Spacer
        self.queueLayout.addItem(QSpacerItem(0,471))

    def toggleQueue(self, event, hide = False):
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
            songs = self.provider.LIST_TRACKS_INFO()
            menu = False
        else:
            songs = self.searchResults
            menu = True
        self.emptyLayout(self.musicLayout)
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
                    pix.loadFromData(requests.get(songs[n]['thumbnail']).content)
                else:
                    pix = QPixmap('sources/%s/%s.jpg' % (self.providerName, songs[n]['id']))
                thumbnail.setPixmap(pix)
                overPicture = QGroupBox(overlay)
                overPicture.move(i * 191 + 15 * i, 0)
                overPicture.setFixedSize(191, 107)
                overPicture.setStyleSheet('')
                overPicture.mouseReleaseEvent = lambda event, n = songs[n] : self.next(self.addToQueue(n['id'], 1), True) if event.button() == Qt.LeftButton else None
                if not menu:
                    overPicture.contextMenuEvent = lambda event, id = songs[n]['id'] : self.downloadedSongDropdown(event, id)
                else:
                    overPicture.contextMenuEvent = lambda event, id = songs[n]['id'] : self.onlineSongsDropdown(event, id)
                title = QLabel(overPicture)
                title.setFixedSize(181, 50)
                title.move(5,5)
                title.setText(songs[n]['title'])
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
        endg = QGroupBox()
        endg.setStyleSheet('background-color: transparent;')
        endg.move(0, y)
        endg.setFixedSize(809, 50)
        self.end = QLabel(endg)
        if rows > 4:
            self.end.setText('You\'ve reached the end!')
        elif menu and rows == 0:
            self.end.setText('Searching for music online may take some time. Please be patient.')
        self.end.resize(799, 40)
        self.end.setWordWrap(True)
        self.end.setAlignment(Qt.AlignCenter)
        self.musicLayout.addWidget(endg)
        if rows <= 4:
            self.musicLayout.addItem(QSpacerItem(0, 107 * (4 - rows) + 15 * (4 - rows) - 50))

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
                self.provider.DOWNLOAD_TRACK(id)
                self.triggerMain.clicked.emit()
            threading.Thread(target = download, daemon = True).start()

    def toggleSearch(self):
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
            searchResults = self.provider.SEARCH(terms)
            self.searchResults = []
            for result in searchResults:
                if not 'Music' in result['categories'] and not terms.startswith('http'):
                    continue
                result['id'] = result.get('id')
                result['title'] = result.get('title')
                result['artist'] = result.get('uploader')
                result['thumbnail'] = result.get('thumbnail')
                result['online'] = True
                self.searchResults.append(result)
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

if __name__ == '__main__':
    # Discord RPC
    try:
        rpc = pypresence.Presence('874365581162328115')
        rpc.connect()
        rpc.clear()
        connected = True
    except:
        connected = False

    # Main Window
    app = QApplication(sys.argv)

    MainWindow = QMainWindow()
    window = GUI(MainWindow)

    window.setupUi(MainWindow)
    window.setup()

    MainWindow.show()

    sys.exit(app.exec_())
