from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Global import Global
import json
import os


def readDataFromJson(path):
    # Проверяем есть ли файл
    if os.path.exists(path):
        # Проверяем не пустой ли он
        if os.path.getsize(path) > 0:
            # Открываем
            with open(path, 'r') as read_file:
                data = json.load(read_file)
        else:
            return False
    else:
        return False
    return data

class ui_LogsSeeWindow(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setupUi()
        self.init_gui()

    def setupUi(self):
        self.resize(Global.Window_width, Global.Window_heigth)

        # Кнопка назад
        self.PushButtonBack = QPushButton(self)
        self.PushButtonBack.setText(Global.ButtonBackText)
        self.PushButtonBack.setGeometry(QRect(Global.ButtonBackGeometryL,
                                                     Global.ButtonBackGeometryT,
                                                     Global.ButtonBackGeometryW,
                                                     Global.ButtonBackGeometryH))
        self.PushButtonBack.setObjectName("Back")

        dir = Global.pathLogs
        files = os.listdir(dir)
        numLogs = 0
        for file in files:
            filename, file_extension = os.path.splitext(file)
            if file_extension == '.json':
                numLogs += 1

        self.labelName = QLabel(self)
        self.labelName.setGeometry(120, 50, 400, 100)
        self.labelName.setText("Всего событий: " + str(numLogs))

        self.table = QTableWidget(self)  # Создаём таблицу
        self.table.setColumnCount(5)     # Устанавливаем три колонки
        self.table.setRowCount(numLogs)        # и одну строку в таблице
        self.table.setGeometry(120, 130, 600, 320)
        self.table.setHorizontalHeaderLabels(['Название', 'Дата', 'Время', 'Камера', 'Просмотр'])

        i = 0
        for file in files:
            filename, file_extension = os.path.splitext(file)
            if file_extension == '.json':
                data = readDataFromJson(dir + '/' + file)
                name = data['video_name']
                date = data['time_stamp']['day'] + ' ' + data['time_stamp']['month'] + ' ' + data['time_stamp']['year']
                time = data['time_stamp']['hour'] + ':' + data['time_stamp']['minutes'] + ':' + data['time_stamp']['seconds']
                camera = data['camera_name']
                video = dir + '/' + name

                self.button = QPushButton(self)
                self.button.setText("Просмотр")
                self.button.clicked.connect(lambda: self.openVideo(video))
                self.button.setObjectName('Open')
                self.button.setFixedSize(115, 30)
                self.button.setObjectName('openVideo')


                self.table.setItem(i, 0, QTableWidgetItem(name))
                self.table.setItem(i, 1, QTableWidgetItem(date))
                self.table.setItem(i, 2, QTableWidgetItem(time))
                self.table.setItem(i, 3, QTableWidgetItem(camera))
                self.table.setCellWidget(i, 4, self.button)
                header = self.table.horizontalHeader()
                header.setSectionResizeMode(QHeaderView.Stretch)
                header.setStretchLastSection(True)
                i += 1

        self.PushButtonBack.clicked.connect(self.Back)

    def init_gui(self):
        self.setStyleSheet(open("style.qss", "r").read())

    def openVideo(self, filename):
        os.startfile(filename)

    def Back(self):
        Global.StackWidgets.setCurrentIndex(0)