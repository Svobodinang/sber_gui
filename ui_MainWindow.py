from PyQt5 import QtCore, QtGui, QtWidgets
from Global import Global


class ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(QtWidgets.QWidget, self).__init__(parent)
        self.setupUi()
        self.init_gui()

    def setupUi(self):
        self.resize(500, 450)

        #камеры
        self.ButtonCamerasSettings = QtWidgets.QPushButton(self)
        self.ButtonCamerasSettings.setText("Настройки камер")
        self.ButtonCamerasSettings.setGeometry(QtCore.QRect(100, 80, 300, 70))
        self.ButtonCamerasSettings.clicked.connect(self.OpenWindowCamerasSettings)

        #детекторы
        # self.ButtonDetectorsSettings = QtWidgets.QPushButton(self)
        # self.ButtonDetectorsSettings.setText("Настройка детекторов")
        # self.ButtonDetectorsSettings.setGeometry(QtCore.QRect(150, 200, 300, 100))

        #настрока логов
        self.ButtonLogsSettings = QtWidgets.QPushButton(self)
        self.ButtonLogsSettings.setText("Настройка логов")
        self.ButtonLogsSettings.setGeometry(QtCore.QRect(100, 180, 300, 70))

        #просмотр логов
        self.ButtonLogsSee = QtWidgets.QPushButton(self)
        self.ButtonLogsSee.setText("Просмотр логов")
        self.ButtonLogsSee.setGeometry(QtCore.QRect(100, 280, 300, 70))



        self.ButtonCamerasSettings.clicked.connect(self.OpenWindowCamerasSettings)
        # self.ButtonDetectorsSettings.clicked.connect(self.OpenWindowDetectorsSettings)
        self.ButtonLogsSettings.clicked.connect(self.OpenWindowLogsSettings)
        self.ButtonLogsSee.clicked.connect(self.OpenWindowLogsSee)

    def init_gui(self):
        self.setStyleSheet(open("style.qss", "r").read())


    def OpenWindowCamerasSettings(self):
        Global.StackWidgets.setCurrentIndex(1)

    def OpenWindowDetectorsSettings(self):
        Global.StackWidgets.setCurrentIndex(2)

    def OpenWindowLogsSettings(self):
        Global.StackWidgets.setCurrentIndex(3)

    def OpenWindowLogsSee(self):
        Global.StackWidgets.setCurrentIndex(4)
