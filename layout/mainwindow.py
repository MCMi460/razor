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
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setGeometry(QtCore.QRect(0, 0, 961, 601))
        self.centralwidget.setObjectName("centralwidget")
        self.themeButton = QtWidgets.QPushButton(self.centralwidget)
        self.themeButton.setGeometry(QtCore.QRect(899, 543, 51, 51))
        self.themeButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.themeButton.setText("")
        self.themeButton.setObjectName("themeButton")
        self.sidePlayer = QtWidgets.QGroupBox(self.centralwidget)
        self.sidePlayer.setGeometry(QtCore.QRect(0, 0, 120, 601))
        self.sidePlayer.setTitle("")
        self.sidePlayer.setFlat(True)
        self.sidePlayer.setObjectName("sidePlayer")
        self.progressBar = QtWidgets.QSlider(self.sidePlayer)
        self.progressBar.setGeometry(QtCore.QRect(10, 60, 31, 501))
        self.progressBar.setMaximum(1000)
        self.progressBar.setSingleStep(0)
        self.progressBar.setPageStep(0)
        self.progressBar.setOrientation(QtCore.Qt.Vertical)
        self.progressBar.setInvertedAppearance(True)
        self.progressBar.setTickInterval(1000)
        self.progressBar.setObjectName("progressBar")
        self.playButton = QtWidgets.QPushButton(self.sidePlayer)
        self.playButton.setGeometry(QtCore.QRect(52, 278, 45, 45))
        self.playButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.playButton.setText("")
        self.playButton.setObjectName("playButton")
        self.backButton = QtWidgets.QPushButton(self.sidePlayer)
        self.backButton.setGeometry(QtCore.QRect(57, 220, 35, 35))
        self.backButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.backButton.setText("")
        self.backButton.setObjectName("backButton")
        self.forwardButton = QtWidgets.QPushButton(self.sidePlayer)
        self.forwardButton.setGeometry(QtCore.QRect(57, 346, 35, 35))
        self.forwardButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.forwardButton.setText("")
        self.forwardButton.setObjectName("forwardButton")
        self.shuffleButton = QtWidgets.QPushButton(self.sidePlayer)
        self.shuffleButton.setGeometry(QtCore.QRect(57, 162, 35, 35))
        self.shuffleButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.shuffleButton.setText("")
        self.shuffleButton.setObjectName("shuffleButton")
        self.loopButton = QtWidgets.QPushButton(self.sidePlayer)
        self.loopButton.setGeometry(QtCore.QRect(57, 404, 35, 35))
        self.loopButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.loopButton.setText("")
        self.loopButton.setObjectName("loopButton")
        self.queueButton = QtWidgets.QPushButton(self.sidePlayer)
        self.queueButton.setGeometry(QtCore.QRect(57, 550, 35, 35))
        self.queueButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.queueButton.setText("")
        self.queueButton.setObjectName("queueButton")
        self.currentTime = QtWidgets.QLabel(self.sidePlayer)
        self.currentTime.setGeometry(QtCore.QRect(2, 37, 49, 20))
        self.currentTime.setAlignment(QtCore.Qt.AlignCenter)
        self.currentTime.setObjectName("currentTime")
        self.endTime = QtWidgets.QLabel(self.sidePlayer)
        self.endTime.setGeometry(QtCore.QRect(1, 570, 49, 20))
        self.endTime.setAlignment(QtCore.Qt.AlignCenter)
        self.endTime.setObjectName("endTime")
        self.musicArea = QtWidgets.QScrollArea(self.centralwidget)
        self.musicArea.setGeometry(QtCore.QRect(120, 80, 841, 521))
        self.musicArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.musicArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.musicArea.setWidgetResizable(True)
        self.musicArea.setObjectName("musicArea")
        self.musicContents = QtWidgets.QWidget()
        self.musicContents.setGeometry(QtCore.QRect(0, 0, 839, 519))
        self.musicContents.setObjectName("musicContents")
        self.musicArea.setWidget(self.musicContents)
        self.queueArea = QtWidgets.QScrollArea(self.centralwidget)
        self.queueArea.setGeometry(QtCore.QRect(114, 80, 142, 521))
        self.queueArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.queueArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.queueArea.setWidgetResizable(True)
        self.queueArea.setObjectName("queueArea")
        self.queueContents = QtWidgets.QWidget()
        self.queueContents.setGeometry(QtCore.QRect(0, 0, 140, 519))
        self.queueContents.setObjectName("queueContents")
        self.queueArea.setWidget(self.queueContents)
        self.searchSection = QtWidgets.QGroupBox(self.centralwidget)
        self.searchSection.setGeometry(QtCore.QRect(880, 0, 81, 81))
        self.searchSection.setTitle("")
        self.searchSection.setObjectName("searchSection")
        self.searchButton = QtWidgets.QPushButton(self.searchSection)
        self.searchButton.setGeometry(QtCore.QRect(10, 10, 61, 61))
        self.searchButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.searchButton.setText("")
        self.searchButton.setObjectName("searchButton")
        self.clearButton = QtWidgets.QPushButton(self.centralwidget)
        self.clearButton.setGeometry(QtCore.QRect(125, 560, 121, 31))
        self.clearButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.clearButton.setObjectName("clearButton")
        self.menuBar = QtWidgets.QMenuBar(self.centralwidget)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 961, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuRazor = QtWidgets.QMenu(self.menuBar)
        self.menuRazor.setObjectName("menuRazor")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.topMenu = QtWidgets.QStackedWidget(self.centralwidget)
        self.topMenu.setGeometry(QtCore.QRect(120, 0, 841, 81))
        self.topMenu.setObjectName("topMenu")
        self.metaStack = QtWidgets.QWidget()
        self.metaStack.setObjectName("metaStack")
        self.songMetadata = QtWidgets.QGroupBox(self.metaStack)
        self.songMetadata.setGeometry(QtCore.QRect(0, 0, 761, 81))
        self.songMetadata.setTitle("")
        self.songMetadata.setObjectName("songMetadata")
        self.thumbnailLabel = QtWidgets.QLabel(self.songMetadata)
        self.thumbnailLabel.setGeometry(QtCore.QRect(10, 10, 109, 61))
        self.thumbnailLabel.setText("")
        self.thumbnailLabel.setObjectName("thumbnailLabel")
        self.uploaderLabel = QtWidgets.QLabel(self.songMetadata)
        self.uploaderLabel.setGeometry(QtCore.QRect(130, 50, 381, 16))
        self.uploaderLabel.setText("")
        self.uploaderLabel.setObjectName("uploaderLabel")
        self.volumeSlider = QtWidgets.QSlider(self.songMetadata)
        self.volumeSlider.setGeometry(QtCore.QRect(550, 30, 160, 21))
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(128)
        self.volumeSlider.setProperty("value", 64)
        self.volumeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.volumeSlider.setTickInterval(1)
        self.volumeSlider.setObjectName("volumeSlider")
        self.volumeMax = QtWidgets.QLabel(self.songMetadata)
        self.volumeMax.setGeometry(QtCore.QRect(720, 30, 20, 20))
        self.volumeMax.setText("")
        self.volumeMax.setObjectName("volumeMax")
        self.volumeMin = QtWidgets.QLabel(self.songMetadata)
        self.volumeMin.setGeometry(QtCore.QRect(520, 30, 20, 20))
        self.volumeMin.setText("")
        self.volumeMin.setObjectName("volumeMin")
        self.titleArea = QtWidgets.QScrollArea(self.songMetadata)
        self.titleArea.setGeometry(QtCore.QRect(130, 20, 381, 25))
        self.titleArea.setStyleSheet("border: 0px solid transparent;")
        self.titleArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.titleArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.titleArea.setWidgetResizable(True)
        self.titleArea.setObjectName("titleArea")
        self.titleContents = QtWidgets.QWidget()
        self.titleContents.setGeometry(QtCore.QRect(0, 0, 381, 25))
        self.titleContents.setStyleSheet("background-color: transparent;")
        self.titleContents.setObjectName("titleContents")
        self.titleLabel = QtWidgets.QLabel(self.titleContents)
        self.titleLabel.setGeometry(QtCore.QRect(0, 0, 600, 25))
        self.titleLabel.setText("")
        self.titleLabel.setObjectName("titleLabel")
        self.titleArea.setWidget(self.titleContents)
        self.topMenu.addWidget(self.metaStack)
        self.searchStack = QtWidgets.QWidget()
        self.searchStack.setObjectName("searchStack")
        self.searchBox = QtWidgets.QGroupBox(self.searchStack)
        self.searchBox.setGeometry(QtCore.QRect(0, 0, 761, 81))
        self.searchBox.setTitle("")
        self.searchBox.setObjectName("searchBox")
        self.searchBar = QtWidgets.QLineEdit(self.searchBox)
        self.searchBar.setGeometry(QtCore.QRect(65, 30, 631, 21))
        self.searchBar.setObjectName("searchBar")
        self.loadingGif = QtWidgets.QLabel(self.searchBox)
        self.loadingGif.setGeometry(QtCore.QRect(720, 30, 21, 21))
        self.loadingGif.setText("")
        self.loadingGif.setObjectName("loadingGif")
        self.topMenu.addWidget(self.searchStack)
        self.playlistArea = QtWidgets.QScrollArea(self.centralwidget)
        self.playlistArea.setGeometry(QtCore.QRect(120, 80, 841, 521))
        self.playlistArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.playlistArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.playlistArea.setWidgetResizable(True)
        self.playlistArea.setObjectName("playlistArea")
        self.playlistContents = QtWidgets.QWidget()
        self.playlistContents.setGeometry(QtCore.QRect(0, 0, 839, 519))
        self.playlistContents.setObjectName("playlistContents")
        self.playlistTitle = QtWidgets.QLabel(self.playlistContents)
        self.playlistTitle.setGeometry(QtCore.QRect(260, 10, 561, 41))
        self.playlistTitle.setText("")
        self.playlistTitle.setObjectName("playlistTitle")
        self.playlistThumbnail = QtWidgets.QLabel(self.playlistContents)
        self.playlistThumbnail.setGeometry(QtCore.QRect(20, 10, 229, 128))
        self.playlistThumbnail.setText("")
        self.playlistThumbnail.setObjectName("playlistThumbnail")
        self.playlistDescription = QtWidgets.QLabel(self.playlistContents)
        self.playlistDescription.setGeometry(QtCore.QRect(260, 80, 561, 58))
        self.playlistDescription.setText("")
        self.playlistDescription.setObjectName("playlistDescription")
        self.playlistTitle_2 = QtWidgets.QLabel(self.playlistContents)
        self.playlistTitle_2.setGeometry(QtCore.QRect(260, 50, 561, 21))
        self.playlistTitle_2.setText("")
        self.playlistTitle_2.setObjectName("playlistTitle_2")
        self.playlistArea.setWidget(self.playlistContents)
        self.sidePlayer.raise_()
        self.musicArea.raise_()
        self.queueArea.raise_()
        self.clearButton.raise_()
        self.topMenu.raise_()
        self.searchSection.raise_()
        self.menuBar.raise_()
        self.themeButton.raise_()
        self.playlistArea.raise_()
        self.a_showSource = QtWidgets.QAction(MainWindow)
        self.a_showSource.setObjectName("a_showSource")
        self.a_closeApp = QtWidgets.QAction(MainWindow)
        self.a_closeApp.setObjectName("a_closeApp")
        self.a_issue = QtWidgets.QAction(MainWindow)
        self.a_issue.setObjectName("a_issue")
        self.a_settings = QtWidgets.QAction(MainWindow)
        self.a_settings.setObjectName("a_settings")
        self.a_credits = QtWidgets.QAction(MainWindow)
        self.a_credits.setObjectName("a_credits")
        self.a_newPlaylist = QtWidgets.QAction(MainWindow)
        self.a_newPlaylist.setObjectName("a_newPlaylist")
        self.a_playlistYoutube = QtWidgets.QAction(MainWindow)
        self.a_playlistYoutube.setObjectName("a_playlistYoutube")
        self.menuRazor.addAction(self.a_settings)
        self.menuRazor.addAction(self.a_credits)
        self.menuRazor.addAction(self.a_closeApp)
        self.menuHelp.addAction(self.a_issue)
        self.menuFile.addAction(self.a_showSource)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.a_newPlaylist)
        self.menuFile.addAction(self.a_playlistYoutube)
        self.menuBar.addAction(self.menuRazor.menuAction())
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Razor Music Player"))
        self.currentTime.setText(_translate("MainWindow", "0:00"))
        self.endTime.setText(_translate("MainWindow", "0:00"))
        self.clearButton.setText(_translate("MainWindow", "Clear Queue"))
        self.menuRazor.setTitle(_translate("MainWindow", "Razor"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.a_showSource.setText(_translate("MainWindow", "Show Source Directory"))
        self.a_closeApp.setText(_translate("MainWindow", "Exit"))
        self.a_issue.setText(_translate("MainWindow", "File an issue"))
        self.a_settings.setText(_translate("MainWindow", "Settings"))
        self.a_credits.setText(_translate("MainWindow", "About"))
        self.a_newPlaylist.setText(_translate("MainWindow", "New Playlist"))
        self.a_playlistYoutube.setText(_translate("MainWindow", "Playlist from Youtube"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())