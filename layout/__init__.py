# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 600)
        self.sidePlayer = QtWidgets.QGroupBox(MainWindow)
        self.sidePlayer.setGeometry(QtCore.QRect(0, 0, 120, 601))
        self.sidePlayer.setTitle("")
        self.sidePlayer.setObjectName("sidePlayer")
        self.progressBar = QtWidgets.QSlider(self.sidePlayer)
        self.progressBar.setGeometry(QtCore.QRect(10, 10, 31, 581))
        self.progressBar.setMaximum(1000)
        self.progressBar.setOrientation(QtCore.Qt.Vertical)
        self.progressBar.setInvertedAppearance(True)
        self.progressBar.setTickInterval(1000)
        self.progressBar.setObjectName("progressBar")
        self.playButton = QtWidgets.QPushButton(self.sidePlayer)
        self.playButton.setGeometry(QtCore.QRect(52, 278, 45, 45))
        self.playButton.setText("")
        self.playButton.setObjectName("playButton")
        self.backButton = QtWidgets.QPushButton(self.sidePlayer)
        self.backButton.setGeometry(QtCore.QRect(57, 220, 35, 35))
        self.backButton.setText("")
        self.backButton.setObjectName("backButton")
        self.forwardButton = QtWidgets.QPushButton(self.sidePlayer)
        self.forwardButton.setGeometry(QtCore.QRect(57, 346, 35, 35))
        self.forwardButton.setText("")
        self.forwardButton.setObjectName("forwardButton")
        self.shuffleButton = QtWidgets.QPushButton(self.sidePlayer)
        self.shuffleButton.setGeometry(QtCore.QRect(57, 162, 35, 35))
        self.shuffleButton.setText("")
        self.shuffleButton.setObjectName("shuffleButton")
        self.loopButton = QtWidgets.QPushButton(self.sidePlayer)
        self.loopButton.setGeometry(QtCore.QRect(57, 404, 35, 35))
        self.loopButton.setText("")
        self.loopButton.setObjectName("loopButton")
        self.songMetadata = QtWidgets.QGroupBox(MainWindow)
        self.songMetadata.setGeometry(QtCore.QRect(120, 0, 661, 81))
        self.songMetadata.setTitle("")
        self.songMetadata.setObjectName("songMetadata")
        self.thumbnailLabel = QtWidgets.QLabel(self.songMetadata)
        self.thumbnailLabel.setGeometry(QtCore.QRect(10, 10, 109, 61))
        self.thumbnailLabel.setText("")
        self.thumbnailLabel.setObjectName("thumbnailLabel")
        self.titleLabel = QtWidgets.QLabel(self.songMetadata)
        self.titleLabel.setGeometry(QtCore.QRect(130, 20, 231, 16))
        self.titleLabel.setText("")
        self.titleLabel.setObjectName("titleLabel")
        self.uploaderLabel = QtWidgets.QLabel(self.songMetadata)
        self.uploaderLabel.setGeometry(QtCore.QRect(130, 40, 231, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.uploaderLabel.setFont(font)
        self.uploaderLabel.setText("")
        self.uploaderLabel.setObjectName("uploaderLabel")
        self.volumeSlider = QtWidgets.QSlider(self.songMetadata)
        self.volumeSlider.setGeometry(QtCore.QRect(450, 30, 160, 21))
        self.volumeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.volumeSlider.setObjectName("volumeSlider")
        self.volumeMax = QtWidgets.QLabel(self.songMetadata)
        self.volumeMax.setGeometry(QtCore.QRect(620, 30, 31, 20))
        self.volumeMax.setText("")
        self.volumeMax.setObjectName("volumeMax")
        self.volumeMin = QtWidgets.QLabel(self.songMetadata)
        self.volumeMin.setGeometry(QtCore.QRect(410, 30, 31, 20))
        self.volumeMin.setText("")
        self.volumeMin.setObjectName("volumeMin")
        self.searchSection = QtWidgets.QGroupBox(MainWindow)
        self.searchSection.setGeometry(QtCore.QRect(780, 0, 181, 81))
        self.searchSection.setTitle("")
        self.searchSection.setObjectName("searchSection")
        self.searchBox = QtWidgets.QGroupBox(self.searchSection)
        self.searchBox.setGeometry(QtCore.QRect(10, 20, 161, 41))
        self.searchBox.setTitle("")
        self.searchBox.setObjectName("searchBox")
        self.searchIcon = QtWidgets.QLabel(self.searchBox)
        self.searchIcon.setGeometry(QtCore.QRect(10, 13, 16, 16))
        self.searchIcon.setText("")
        self.searchIcon.setObjectName("searchIcon")
        self.searchInput = QtWidgets.QLineEdit(self.searchBox)
        self.searchInput.setGeometry(QtCore.QRect(32, 10, 121, 24))
        self.searchInput.setObjectName("searchInput")
        self.musicArea = QtWidgets.QScrollArea(MainWindow)
        self.musicArea.setGeometry(QtCore.QRect(120, 80, 841, 521))
        self.musicArea.setWidgetResizable(True)
        self.musicArea.setObjectName("musicArea")
        self.musicContents = QtWidgets.QWidget()
        self.musicContents.setGeometry(QtCore.QRect(0, 0, 839, 519))
        self.musicContents.setObjectName("musicContents")
        self.musicArea.setWidget(self.musicContents)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Razor Music Player"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
