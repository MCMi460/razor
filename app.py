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

    def setup(self):
        # Images
        images = {
            'qss': '',
            'playImage': 'play.png',
            'pauseImage': 'pause.png',
            'loopImage': 'loop.png',
            'backImage': 'rewind.png',
            'nextImage': 'skip.png',
        }
        self.lightImages = images.copy()
        self.darkImages = images.copy()
        for type in ('light', 'dark'):
            # QSS Stylesheet (redundancy check?)
            with open('layout/resources/%s/styles.qss' % type, 'r') as file:
                getattr(self, type + 'Images')['qss'] = file.read()
            for key in list(images.keys())[1:]:
                getattr(self, type + 'Images')[key] = QIcon(('layout/resources/%s/' % type) + images[key])

        self.theme = self.darkImages

        # Stylesheet
        self.MainWindow.setStyleSheet(self.theme['qss'])

        # Label images
        self.playButton.setIcon(self.theme['playImage'])
        self.playButton.setIconSize(self.playButton.size())

        self.backButton.setIcon(self.theme['backImage'])
        self.backButton.setIconSize(self.backButton.size())
        self.forwardButton.setIcon(self.theme['nextImage'])
        self.forwardButton.setIconSize(self.forwardButton.size())

        # Push Buttons
        self.playButton.clicked.connect(self.toggle)
        self.forwardButton.clicked.connect(self.next)
        self.backButton.clicked.connect(self.back)

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
                self.addToQueue(id)
            if not id:
                id = self.queue[0]
            threading.Thread(target = self._constantPlay, args = (self.providerName, id,), daemon = True).start()
        self.playButton.setIcon(self.theme['pauseImage'])

    def _constantPlay(self, provider, id):
        con.play(provider, id, False)
        while con.track['media'] and not con.track['media'].is_playing():
            pass
        while con.track['media'] and con.track['media'].get_state() in (vlc.State.Playing, vlc.State.Paused):
            pass
        if con.track['media']:
            self.next()
        else:
            self.stop()

    def next(self):
        if con.track['media']:
            self.stop()
        if len(self.queue) > 0:
            self.backQueue.append(self.queue.pop(0))
        if len(self.queue) > 0:
            self.play(self.queue[0])

    def back(self):
        if con.track['media'] and con.track['media'].get_time() > 2000 and con.track['media'].get_length() > 3000:
            con.track['media'].set_time(0)
        elif con.track['media']:
            self.stop()
            if len(self.backQueue) > 0:
                self.queue.insert(0, self.backQueue.pop(-1))
                if len(self.queue) > 0:
                    self.play(self.queue[0])

    def addToQueue(self, id:str):
        if not id:
            id = random.choice(self.provider.LIST_TRACKS())
        self.queue.append(id)
        return self.queue[0]

    def stop(self):
        try:
            con.stop()
        except:
            pass
        self.playButton.setIcon(self.theme['playImage'])

    def pause(self):
        con.pause()

    def resume(self):
        con.resume()

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
