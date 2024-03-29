# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.resize(600, 400)
        self.settingsLabel = QtWidgets.QLabel(Settings)
        self.settingsLabel.setGeometry(QtCore.QRect(10, 10, 571, 20))
        self.settingsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.settingsLabel.setObjectName("settingsLabel")
        self.fontSizeLabel = QtWidgets.QLabel(Settings)
        self.fontSizeLabel.setGeometry(QtCore.QRect(130, 50, 161, 71))
        self.fontSizeLabel.setObjectName("fontSizeLabel")
        self.fontSize = QtWidgets.QSpinBox(Settings)
        self.fontSize.setGeometry(QtCore.QRect(340, 75, 61, 25))
        self.fontSize.setMinimum(5)
        self.fontSize.setMaximum(20)
        self.fontSize.setProperty("value", 13)
        self.fontSize.setObjectName("fontSize")

        self.retranslateUi(Settings)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Settings"))
        self.settingsLabel.setText(_translate("Settings", "Settings"))
        self.fontSizeLabel.setText(_translate("Settings", "Change font size"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Settings = QtWidgets.QDialog()
    ui = Ui_Settings()
    ui.setupUi(Settings)
    Settings.show()
    sys.exit(app.exec_())
