from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Global import Global
import os.path
from ui_CameraSettingsWindow import ui_CameraSettingsWindow
from ui_AddNewCameraWindow import ui_AddNewCameraWindow
import json


def readDataFromJson(path):
    # Проверяем есть ли файл
    if os.path.exists(path):
        # Проверяем не пустой ли он
        if os.path.getsize(path) > 0:
            # Открываем
            with open(path, 'r') as read_file:
                data = json.load(read_file)
    return data


def writeDataToJson(data, path):
    # Записываем в файл обновленные данные
    with open(path, 'w') as write_file:
        json.dump(data, write_file)


class ui_CamerasWindow(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setupUi()
        self.init_gui()

    def setupUi(self):
        self.resize(600, 600)

        # Кнопка назад
        self.PushButtonBack = QPushButton(self)
        self.PushButtonBack.setText(Global.ButtonBackText)
        self.PushButtonBack.setGeometry(QRect(Global.ButtonBackGeometryL,
                                              Global.ButtonBackGeometryT,
                                              Global.ButtonBackGeometryW,
                                              Global.ButtonBackGeometryH))

        self.PushButtonBack.setObjectName("Back")


        # Создаем виджеты, для того, чтобы можно было задать рзамер layout. Для кнопок камер
        self.LayoutWidgetCameras = QWidget(self)
        self.LayoutWidgetCameras.setGeometry(80, 50, 200, 400)
        # Создаем layout, именно его, чтобы проще было удалять кнопки и добавлять их
        self.layoutCameras = QGridLayout()
        self.LayoutWidgetCameras.setLayout(self.layoutCameras)

        # Аналогично, потому что у нас есть еще поле с кнопками удаления камер
        self.LayoutWidgetDeleteCameras = QWidget(self)
        self.LayoutWidgetDeleteCameras.setGeometry(270, 50, 250, 400)
        self.layoutDeleteCameras = QGridLayout()
        self.LayoutWidgetDeleteCameras.setLayout(self.layoutDeleteCameras)

        # Создаем массивы кнопок камер и кнопок удаления камер
        self.ButtonGroupCameras = QButtonGroup(self)
        self.ButtonGroupDeleteCameras = QButtonGroup(self)
        # Нумерация камер идет с 1, а массив с 0
        for i in range(1, Global.countCameras + 1):
            self.PushButtonCamera = QPushButton(self)
            self.PushButtonCamera.setText("camera " + str(i))
            self.PushButtonCamera.setFixedSize(150, 50)
            self.ButtonGroupCameras.addButton(self.PushButtonCamera)
            self.layoutCameras.addWidget(self.PushButtonCamera)
            self.PushButtonCamera.setObjectName("PushButtonCamera")

            self.PushButtonDeleteCamera = QPushButton(self)
            self.PushButtonDeleteCamera.setText("Удалить камеру")
            self.PushButtonDeleteCamera.setFixedSize(200, 50)
            self.ButtonGroupDeleteCameras.addButton(self.PushButtonDeleteCamera)
            self.layoutDeleteCameras.addWidget(self.PushButtonDeleteCamera)
            self.PushButtonDeleteCamera.setObjectName("PushButtonDeleteCamera")

        idCamera = 1
        for button in self.ButtonGroupCameras.buttons():
            # Заполняем массивы {-2: 1} и {1: -2}. Потому что в массивах кнопок нумерация идет с -2
            Global.idCamerasQtArr[self.ButtonGroupCameras.id(button)] = idCamera
            Global.idCamerasArrQt[idCamera] = self.ButtonGroupCameras.id(button)
            idCamera += 1

        # Кнопка добавления камеры
        self.PushButtonAddCamera = QPushButton(self)
        self.PushButtonAddCamera.setText("Добавить камеру")
        self.PushButtonAddCamera.setGeometry(QRect(360, 520, 200, 50))


        self.PushButtonBack.clicked.connect(self.Back)
        self.ButtonGroupCameras.buttonClicked.connect(self.OpenCameraSettingsWindow)
        self.ButtonGroupDeleteCameras.buttonClicked.connect(self.DeleteCamera)
        self.PushButtonAddCamera.clicked.connect(self.AddCamera)

    def init_gui(self):
        self.setStyleSheet(open("style.qss", "r").read())

    def Back(self):
        Global.StackWidgets.setCurrentIndex(0)

    def OpenCameraSettingsWindow(self, btn):
        Global.numCamera = btn.text().split(" ")[1]
        Global.StackWidgets.addWidget(ui_CameraSettingsWindow())
        Global.StackWidgets.setCurrentIndex(Global.StackWidgets.count() - 1)


    def AddCamera(self):
        Global.StackWidgets.addWidget(ui_AddNewCameraWindow())
        Global.StackWidgets.setCurrentIndex(Global.StackWidgets.count() - 1)


    def DeleteCamera(self, btnDeleteCameraDeleted):
        # Получаем номер удаляемой камеры. Номер в обычно системе счисления и в сс массива кнопок
        idDeletedArrCamera = Global.idCamerasQtArr[self.ButtonGroupDeleteCameras.id(btnDeleteCameraDeleted)]
        idDeletedQtCamera = Global.idCamerasArrQt[idDeletedArrCamera]

        # Удаляем кнопки с виджета
        btnDeleteCameraDeleted.setParent(None)
        btnCameraDeleted = self.ButtonGroupCameras.button(idDeletedQtCamera)
        btnCameraDeleted.setParent(None)

        # Удаляем файл с номером выбранной камеры
        os.remove(Global.pathCamera + "camera" + str(idDeletedArrCamera) + ".json")
        # Зачитываем дынные с файла core.json
        data = readDataFromJson(Global.pathCore)

        # Начиная со следующей после удаленной камеры начинаем менять все что связано с камерами
        for i in range(idDeletedArrCamera + 1, len(Global.idCamerasArrQt) + 1):
            # Меняем текст на кнопке 3 -> 2
            button = self.ButtonGroupCameras.button(Global.idCamerasArrQt[i])
            button.setText("camera" + str(i - 1))

            # Переименовываем файлы в настрйоках камеры 3 -> 2
            os.rename(Global.pathCamera + "camera" + str(i) + ".json",
                      Global.pathCamera + "camera" + str(i - 1) + ".json")

            # Меняем файл core, меняем название 3 -> 2
            data['cameras'][i - 1]['name'] = \
                'camera' + str(i - 1)
            # Меняем путь до файла настроек камеры 3 -> 2
            data['cameras'][i - 1]['config_path'] = \
                'camera/camera' + str(i - 1) + ".json"

        # Из глобального массива удаляем удаленную камеру
        del Global.idCamerasQtArr[idDeletedQtCamera]
        # Меняем массив qt - arr
        for i in range(idDeletedArrCamera + 1, len(Global.idCamerasArrQt) + 1):
            button = self.ButtonGroupCameras.button(Global.idCamerasArrQt[i])
            qtIdButton = self.ButtonGroupCameras.id(button)
            Global.idCamerasQtArr[qtIdButton] = Global.idCamerasQtArr[qtIdButton] - 1

        # Массив arr - qt меняем инвертируя массив qt - arr
        Global.idCamerasArrQt = {v: k for k, v in Global.idCamerasQtArr.items()}

        # Удаляем нажатую камеру из core
        data['cameras'].pop(idDeletedArrCamera - 1)

        # Записываем обновленные данные в core
        writeDataToJson(data, Global.pathCore)

        # Удалаем камеру из массива кнопок
        self.ButtonGroupDeleteCameras.removeButton(btnDeleteCameraDeleted)
        # Удаляем кнопку удаления из массива
        self.ButtonGroupCameras.removeButton(btnCameraDeleted)
        # Изменяем количество камер на -1
        Global.countCameras -= 1




