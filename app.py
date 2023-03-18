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

    def setup(self):
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
        }
        pixmaps = {
            'blankThumbnail': 'thumbnail.png',
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
        self.forwardButton.clicked.connect(self.next)
        self.backButton.clicked.connect(self.back)
        self.loopButton.clicked.connect(self.loop)
        self.themeButton.clicked.connect(self.toggleTheme)

        self.progressBar.sliderReleased.connect(self.updateDuration)

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

    def _constantPlay(self, provider, id):
        con.play(provider, id, False)
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

    def next(self):
        if con.track['media']:
            self.stop()
        if not self.looping:
            if len(self.queue) > 0:
                self.backQueue.append(self.queue.pop(0))
            if len(self.queue) > 0:
                self.play(self.queue[0])
        else:
            if len(self.queue) > 0:
                self.play(self.queue[0])

    def back(self):
        if con.track['media'] and ( (con.track['media'].get_time() > 2000 and con.track['media'].get_length() > 3000) or self.looping ):
            con.track['media'].set_time(0)
        elif con.track['media']:
            self.stop()
        if len(self.backQueue) > 0:
            self.queue.insert(0, self.backQueue.pop(-1))
            if len(self.queue) > 0:
                self.play(self.queue[0])


    def addToQueue(self, id:str):
        if not id:
            tracks = self.provider.LIST_TRACKS()
            if len(tracks) == 0:
                raise Exception('no songs!')
            id = random.choice(self.provider.LIST_TRACKS())
        self.queue.append(id)
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
            pix = self.theme['blankThumbnail']
        else:
            pix = QPixmap()
            pix.loadFromData(requests.get(info['thumbnail']).content)
        self.thumbnailLabel.setPixmap(pix)

    def updateProgressBar(self):
        while con.track['media'] and con.track['media'].get_state() in (vlc.State.Playing, vlc.State.Paused):
            self.progressBar.setValue(con.track['media'].get_time())
            time.sleep(1)

    def updateDuration(self):
        if con.track['media']:
            con.track['media'].set_time(self.progressBar.value())
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

        self.loopButton.setIcon(self.theme['loopImage'])
        self.loopButton.setIconSize(self.loopButton.size())
        self.shuffleButton.setIcon(self.theme['shuffleImage'])
        self.shuffleButton.setIconSize(self.shuffleButton.size())

        self.themeButton.setIcon(self.theme['modeImage'])
        self.themeButton.setIconSize(self.themeButton.size())

        self.thumbnailLabel.setScaledContents(True)

        if not con.track['media']:
            self.updateMeta()

        ### STYLESHEET END ###

if __name__ == '__main__':
    # Begin main thread for user
    con = Console()

    # Discord RPC


    # Main Window
    app = QApplication(sys.argv)

    MainWindow = QMainWindow()
    window = GUI(MainWindow)

    window.setupUi(MainWindow)
    window.setup()

    MainWindow.show()

    sys.exit(app.exec_())
