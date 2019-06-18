from PyQt5 import QtCore, QtGui, QtWidgets
from Global import Global


class ui_DetectorsSettingsWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(QtWidgets.QWidget, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.resize(Global.Window_width, Global.Window_heigth)

        self.PushButtonBack = QtWidgets.QPushButton(self)
        self.PushButtonBack.setText(Global.ButtonBackText)
        self.PushButtonBack.setGeometry(QtCore.QRect(Global.ButtonBackGeometryL,
                                                     Global.ButtonBackGeometryT,
                                                     Global.ButtonBackGeometryW,
                                                     Global.ButtonBackGeometryH))

        self.PushButtonBack.clicked.connect(self.OpenMainWindow)

    def OpenMainWindow(self):
        Global.StackWidgets.setCurrentIndex(0)
