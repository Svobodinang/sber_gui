from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from ui_MainWindow import ui_MainWindow
from ui_CamerasWindow import ui_CamerasWindow
from ui_LogsSettingsWindow import ui_LogsSettingsWindow
from ui_DetectorsSettingsWindow import ui_DetectorsSettingsWindow
from ui_LogsSeeWindow import ui_LogsSeeWindow
from Global import Global


class Main(QMainWindow):
    def __init__(self):

        super().__init__()

        self.widget = Global.StackWidgets.addWidget(ui_MainWindow())      # 0
        Global.StackWidgets.addWidget(ui_CamerasWindow())                 # 1
        Global.StackWidgets.addWidget(ui_DetectorsSettingsWindow())       # 2
        Global.StackWidgets.addWidget(ui_LogsSettingsWindow())            # 3
        Global.StackWidgets.addWidget(ui_LogsSeeWindow())                 # 4


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
