# MCMi460 on Github
from subrosa import *
from layout import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Create GUI
class GUI(Ui_MainWindow):
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow

        # Abstract variables
        self.providerName = 'youtube'
        self.provider = con._getProvider(self.providerName)
        self.queue = ['gEbRqpFkTBk','-SyBR-M2YvU',]
        self.backQueue = []
        self.looping = False

        self.cache = {
            'title': '',
            'artist': '',
            'thumbnail': '',
            'id': '',
        }

    def setup(self):
        # Queue Menu
        self.queueArea.hide()
        self.queueLayout = QGridLayout()
        self.queueContents.setLayout(self.queueLayout)
        self.queueUpdate()

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

        self.themeUpdate()

        # Connections
        self.playButton.clicked.connect(self.toggle)
        self.forwardButton.clicked.connect(lambda event : self.next())
        self.backButton.clicked.connect(self.back)
        self.loopButton.clicked.connect(self.loop)
        self.themeButton.clicked.connect(self.toggleTheme)
        self.volumeMax.mouseReleaseEvent = lambda a : self.volumeSlider.setValue(self.volumeSlider.value() + 20)
        self.volumeMin.mouseReleaseEvent = lambda a : self.volumeSlider.setValue(self.volumeSlider.value() - 20)
        self.queueButton.clicked.connect(self.toggleQueue)
        self.shuffleButton.clicked.connect(self.shuffle)

        self.underLyingButton = QPushButton()
        self.underLyingButton.clicked.connect(lambda a : self.queueUpdate(True))

        self.progressBar.sliderReleased.connect(self.updateDuration)
        self.volumeSlider.valueChanged.connect(self.updateVolume)

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

    def addToQueue(self, id:str):
        if not id:
            tracks = self.provider.LIST_TRACKS()
            if len(tracks) == 0:
                raise Exception('no songs!')
            id = random.choice(self.provider.LIST_TRACKS())
        self.queue.append(id)
        self.queueUpdate()
        return self.queue[0]

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
            if connected: rpc.clear()
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
            if connected: rpc.clear()
        else:
            if connected: rpc.update(**dict)

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
                group.setCursor(QCursor(Qt.PointingHandCursor))
                label = QLabel(group)
                label.move(5,5)
                label.resize(109, 61)
                pix = QPixmap('sources/%s/%s.jpg' % (self.providerName, self.queue[i]))
                label.setPixmap(pix)
                label.setScaledContents(True)
                label.mouseReleaseEvent = lambda event, i=i : self.next(i, True)
                self.queueLayout.addWidget(group)
                y += 80
            self.queueLayout.addItem(QSpacerItem(0,521))

    def toggleQueue(self):
        if self.queueArea.isVisible():
            self.queueArea.hide()
        else:
            self.queueArea.show()

    def shuffle(self):
        if len(self.queue) > 1:
            list = self.queue[1:]
            random.shuffle(list)
            for i in range(1, len(self.queue)):
                self.queue[i] = list[i - 1]
            self.queueUpdate()

if __name__ == '__main__':
    # Begin main thread for user
    con = Console()

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
