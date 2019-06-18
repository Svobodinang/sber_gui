from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Global import Global
import os
import json
import zipfile
import datetime


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


def writeDataToJson(data, path):
    # Записываем в файл обновленные данные
    with open(path, 'w') as write_file:
        json.dump(data, write_file)


class ui_LogsSettingsWindow(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setupUi()
        self.init_gui()

    def setupUi(self):
        self.resize(500, 400)

        self.PushButtonBack = QPushButton(self)
        self.PushButtonBack.setText(Global.ButtonBackText)
        self.PushButtonBack.setGeometry(QRect(Global.ButtonBackGeometryL,
                                              Global.ButtonBackGeometryT,
                                              Global.ButtonBackGeometryW,
                                              Global.ButtonBackGeometryH))
        self.PushButtonBack.setObjectName("Back")

        self.dataCore = readDataFromJson(Global.pathCore)
        Global.pathLogs = self.dataCore['log_path']

        self.label = QLabel(self)
        self.label.setText("Путь до логов:")
        self.label.setGeometry(70, 80, 400, 30)
        self.label.setObjectName("labelSmall")

        self.labelPath = QLabel(self)
        self.labelPath.setText(Global.pathLogs)
        self.labelPath.setGeometry(70, 110, 400, 30)
        self.labelPath.setObjectName("labelSmall")

        self.PushButtonBrowseFolder = QPushButton(self)
        self.PushButtonBrowseFolder.setText("Изменить путь до папки с логами")
        self.PushButtonBrowseFolder.setGeometry(50, 180, 400, 50)

        self.PushButtonZipLogs = QPushButton(self)
        self.PushButtonZipLogs.setText("Заархивировать все сохраненные логи")
        self.PushButtonZipLogs.setGeometry(50, 240, 400, 50)

        self.labelStatusZip = QLabel(self)
        self.labelStatusZip.setGeometry(60, 300, 400, 50)
        self.labelStatusZip.setObjectName("labelSmall")

        self.PushButtonBack.clicked.connect(self.OpenMainWindow)
        self.PushButtonBrowseFolder.clicked.connect(self.BrowseFolder)
        self.PushButtonZipLogs.clicked.connect(self.ZipLogs)

    def init_gui(self):
        self.setStyleSheet(open("style.qss", "r").read())

    def OpenMainWindow(self):
        Global.StackWidgets.setCurrentIndex(0)

    def BrowseFolder(self):
        directory = QFileDialog.getExistingDirectory(self, "Выберите папку")
        Global.pathLogs = directory
        self.dataCore['log_path'] = directory
        writeDataToJson(self.dataCore, Global.pathCore)
        self.labelPath.setText(Global.pathLogs)

    def ZipLogs(self):
        self.labelStatusZip.setText("Логи архивируются")
        self.repaint()
        new_zip = zipfile.ZipFile(Global.pathLogs + "-" + str(datetime.date.today()) + ".zip", 'w')

        for root, dirs, files in os.walk(Global.pathLogs):  # Список всех файлов и папок в директории folder
            for file in files:
                new_zip.write(os.path.join(root, file), file)  # Создание относительных путей и запись файлов в архив

        new_zip.close()
        self.labelStatusZip.setText("Логи заархивированы")



