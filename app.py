# MCMi460 on Github
from subrosa import *
from layout import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# QSS Stylesheet (redundancy check?)
with open('styles.qss', 'r') as file:
    qss = file.read()

# Create GUI
class GUI(Ui_MainWindow):
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow

    def setup(self):
        # Stylesheet
        self.MainWindow.setStyleSheet(qss)

        # Images
        images = {
            'playImage': 'layout/resources/!/play.png',
            'pauseImage': 'layout/resources/!/pause.png',
            'loopImage': 'layout/resources/!/loop.png',
        }
        self.lightImages = images.copy()
        self.darkImages = images.copy()
        for type in ('light', 'dark'):
            for key in images:
                getattr(self, type + 'Images')[key] = QIcon(images[key].replace('!', type))

        # Label images
        self.playButton.setIcon(self.lightImages['playImage'])
        self.playButton.setIconSize(self.playButton.size())

        # Push Buttons
        self.playButton.clicked.connect(self.toggle)

    def toggle(self):
        if con.track['media'] and con.track['media'].is_playing():
            self.pause()
            self.playButton.setIcon(self.lightImages['playImage'])
        else:
            self.play()
            self.playButton.setIcon(self.lightImages['pauseImage'])

    def play(self):
        if con.track['media']:
            con.resume()
        else:
            con.play('youtube', random.choice(con._getProvider('youtube').LIST_TRACKS()))
        self.playButton

    def stop(self):
        con.stop()

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
