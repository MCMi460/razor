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
