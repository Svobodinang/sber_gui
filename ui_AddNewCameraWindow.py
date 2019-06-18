from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PIL.ImageQt import ImageQt
from Global import Global
import json
import os
import rtsp
from ui_AddBlackRectWindow import ui_AddBlackRectWindow
from ui_AddWhiteRectWindow import ui_AddWhiteRectWindow
from ui_AddMaskWindow import ui_AddMaskWindow


def writeDataToJson(data, path):
    # Записываем в файл обновленные данные
    with open(path, 'w') as write_file:
        json.dump(data, write_file)

def readDataFromJson(path):
    # Проверяем есть ли файл
    if os.path.exists(path):
        # Проверяем не пустой ли он
        if os.path.getsize(path) > 0:
            # Открываем
            with open(path, 'r') as read_file:
                data = json.load(read_file)
    return data

def checkParametersCamera(user, passwd, ip, port):
    # Формируем ссылку на камеру
    ref = "rtsp://" + user + ":" + passwd + "@" + ip + ":554/ISAPI/Streaming/Channels/101"

    # Пингуем ip камеры
    response = os.system("ping " + ip)
    # Если пинг прошел успешно
    if response == 0:
        # Пытаемся получить изображение с камеры
        try:
            Global.client = rtsp.Client(rtsp_server_uri=ref)
        # Если не удалось получить, значит пароль или логин неправильный, меняем флаг
        except:
            return 0
        return 1
    else:
        return -1


class ui_AddNewCameraWindow(QWidget):
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

        self.PushButtonSaveChanged = QPushButton(self)
        self.PushButtonSaveChanged.setText("Сохранить изменения")
        self.PushButtonSaveChanged.setGeometry(QRect(100, 350, 250, 50))

        self.LabelStatusSaved = QLabel(self)
        self.LabelStatusSaved.setGeometry(QRect(380, 350, 350, 50))
        self.LabelStatusSaved.setObjectName("Status")

        # Создаем виджеты, для того, чтобы можно было задать рзамер layout. Для подписей
        self.LayoutWidgetLabels = QWidget(self)
        self.LayoutWidgetLabels.setGeometry(130, 100, 200, 200)
        self.layoutLabels = QGridLayout()
        self.LayoutWidgetLabels.setLayout(self.layoutLabels)

        # Создаем виджеты, для того, чтобы можно было задать рзамер layout. Для полей настроек
        self.LayoutWidgetLineEdit = QWidget(self)
        self.LayoutWidgetLineEdit.setGeometry(230, 100, 200, 200)
        self.layoutLineEdit = QGridLayout()
        self.LayoutWidgetLineEdit.setLayout(self.layoutLineEdit)

        self.labelIp = QLabel(self)
        self.labelIp.setText('Ip')
        self.layoutLabels.addWidget(self.labelIp)
        self.lineEditIp = QLineEdit(self)
        self.layoutLineEdit.addWidget(self.lineEditIp)

        self.labelPort = QLabel(self)
        self.labelPort.setText('Порт')
        self.layoutLabels.addWidget(self.labelPort)
        self.lineEditPort = QLineEdit(self)
        self.lineEditPort.setText('')
        self.layoutLineEdit.addWidget(self.lineEditPort)
        # self.lineEditPort.setDisabled(True)

        self.labelUser = QLabel(self)
        self.labelUser.setText('User')
        self.layoutLabels.addWidget(self.labelUser)
        self.lineEditUser = QLineEdit(self)
        self.layoutLineEdit.addWidget(self.lineEditUser)

        self.labelPassword = QLabel(self)
        self.labelPassword.setText('Пароль')
        self.layoutLabels.addWidget(self.labelPassword)
        self.lineEditPassword = QLineEdit(self)
        self.layoutLineEdit.addWidget(self.lineEditPassword)

        self.data = Global.dataCameraEmpty

        # Создание кнопок добавления маски и ректанглов
        self.LayoutWidgetButtons = QWidget(self)
        self.LayoutWidgetButtons.setGeometry(450, 100, 320, 200)
        self.layoutButtons = QGridLayout(self)
        self.LayoutWidgetButtons.setLayout(self.layoutButtons)

        self.ButtonAddBlackRect = QPushButton(self)
        self.ButtonAddBlackRect.setText("Добавить области на черном фоне")
        self.ButtonAddBlackRect.setFixedSize(300, 40)

        self.ButtonAddWhiteRect = QPushButton(self)
        self.ButtonAddWhiteRect.setText("Добавить области на белом фоне")
        self.ButtonAddWhiteRect.setFixedSize(300, 40)

        self.ButtonAddMask = QPushButton(self)
        self.ButtonAddMask.setText("Добавить черную маску")
        self.ButtonAddMask.setFixedSize(300, 40)

        self.ButtonAddBlackRect.setObjectName("addRect")
        self.ButtonAddMask.setObjectName("addRect")
        self.ButtonAddWhiteRect.setObjectName("addRect")

        self.layoutButtons.addWidget(self.ButtonAddBlackRect)
        self.layoutButtons.addWidget(self.ButtonAddWhiteRect)
        self.layoutButtons.addWidget(self.ButtonAddMask)
        # Объявляем кнопки добавления ректанглов не действительными
        self.ButtonAddBlackRect.setDisabled(True)
        self.ButtonAddWhiteRect.setDisabled(True)
        self.ButtonAddMask.setDisabled(True)

        self.PushButtonBack.clicked.connect(self.Back)
        self.PushButtonSaveChanged.clicked.connect(self.SaveChanged)
        self.ButtonAddWhiteRect.clicked.connect(self.AddWhiteRect)
        self.ButtonAddBlackRect.clicked.connect(self.AddBlackRect)
        self.ButtonAddMask.clicked.connect(self.AddMask)

    def init_gui(self):
        self.setStyleSheet(open("style.qss", "r").read())

    def SaveChanged(self):
        # Так как пинг происходит долго, информируем пользователя, что идет проверка
        self.LabelStatusSaved.setText("Происходит проверка введенных данных")
        # Для того, чтобы текст высветился, перерисовываем виджет
        self.repaint()

        ip = self.lineEditIp.text()
        port = self.lineEditPort.text()
        user = self.lineEditUser.text()
        passwd = self.lineEditPassword.text()

        # Формируем ссылку на камеру
        ref = "rtsp://" + user + ":" + passwd + "@" + ip + ":554/ISAPI/Streaming/Channels/101"

        # Пингуем ip камеры
        response = os.system("ping " + ip)
        # Создаем флаг, True - правильный логин пароль, False - неправильный
        good = True
        # Если пинг прошел успешно
        if response == 0:
            # Пытаемся получить изображение с камеры
            try:
                client = rtsp.Client(rtsp_server_uri=ref)
                client.read()
            # Если не удалось получить, значит пароль или логин неправильный, меняем флаг
            except:
                good = False
            # Если пароль логин ip верен - меняем
            if good:
                self.LabelStatusSaved.setText("Новые данные сохранены")
                self.data['ip'] = self.lineEditIp.text()
                self.data['port'] = self.lineEditPort.text()
                self.data['user'] = self.lineEditUser.text()
                self.data['password'] = self.lineEditPassword.text()

                Global.ip = ip
                Global.user = user
                Global.passwd = passwd

                # Добавляем количество камер
                Global.countCameras += 1

                # Объявляем новую камеру действующей камерой
                Global.numCamera = Global.countCameras
                # Получаем путь до файла касеры
                self.pathCamera = Global.pathCamera + "camera" + str(Global.numCamera) + ".json"
                # Создаем новый файл для новой камеру и записываем туда данные
                writeDataToJson(self.data, self.pathCamera)

                # Получаем данные из файла core
                dataCore = readDataFromJson(Global.pathCore)
                # Добавляем туда новую камеру
                dataCore['cameras'].append(Global.dataCoreCameraEmpty)
                # Меняем поля название и путь до файла настроек
                dataCore['cameras'][len(dataCore['cameras']) - 1]['name'] = "camera" + str(Global.numCamera)
                dataCore['cameras'][len(dataCore['cameras']) - 1]['config_path'] = "camera/camera" + \
                                                                                str(Global.numCamera) + ".json"
                # Записываем новые данные в файл
                writeDataToJson(dataCore, Global.pathCore)

                # Нужно добавить кнопку новой камеры в окно камер
                # Для этого получаем окно камер
                CameraWindow = Global.StackWidgets.widget(1)
                # Создаем и добавляем кнопку камеры
                PushButtonCamera = QPushButton()
                PushButtonCamera.setText("camera " + str(Global.numCamera))
                PushButtonCamera.setFixedSize(150, 50)
                CameraWindow.ButtonGroupCameras.addButton(PushButtonCamera)
                CameraWindow.layoutCameras.addWidget(PushButtonCamera)

                # Создаем и добавляем кнопку удаления камеры
                PushButtonDeleteCamera = QPushButton()
                PushButtonDeleteCamera.setText("Удалить камеру")
                PushButtonDeleteCamera.setFixedSize(200, 50)
                CameraWindow.ButtonGroupDeleteCameras.addButton(PushButtonDeleteCamera)
                CameraWindow.layoutDeleteCameras.addWidget(PushButtonDeleteCamera)

                PushButtonCamera.setObjectName("PushButtonCamera")
                PushButtonDeleteCamera.setObjectName("PushButtonDeleteCamera")

                # Меняем глобальные массивы соотношения id в массиве кнопок и номера камеры
                Global.idCamerasArrQt[Global.numCamera] = CameraWindow.ButtonGroupDeleteCameras.id(PushButtonDeleteCamera)
                Global.idCamerasQtArr[CameraWindow.ButtonGroupDeleteCameras.id(PushButtonDeleteCamera)] = Global.numCamera

                # Объявляем кнопки добавления ректанглов действительными
                self.ButtonAddBlackRect.setDisabled(False)
                self.ButtonAddWhiteRect.setDisabled(False)
                self.ButtonAddMask.setDisabled(False)

            else:
                self.LabelStatusSaved.setText("Введен неверный логин или пароль")
        else:
            self.LabelStatusSaved.setText("Введен неверный ip")


    def Back(self):
        Global.StackWidgets.setCurrentIndex(1)
        Global.StackWidgets.removeWidget(ui_AddNewCameraWindow())

    def AddWhiteRect(self):
        self.LabelStatusSaved.setText("Происходит проверка параметров камеры")
        self.repaint()

        status = checkParametersCamera(Global.user, Global.passwd, Global.ip, Global.port)
        if status == 1:
            image = Global.client.read()
            qim = ImageQt(image)
            Global.pixmap = QPixmap.fromImage(qim)
            self.LabelStatusSaved.setText("")
            Global.StackWidgetsRects.addWidget(ui_AddWhiteRectWindow())
            Global.StackWidgetsRects.setCurrentIndex(Global.StackWidgetsRects.count() - 1)
        elif status == 0:
            self.LabelStatusSaved.setText("Введен неверный логин или пароль")
        elif status == -1:
            self.LabelStatusSaved.setText("Введен неверный ip")

    def AddBlackRect(self):
        self.LabelStatusSaved.setText("Происходит проверка параметров камеры")
        self.repaint()

        status = checkParametersCamera(Global.user, Global.passwd, Global.ip, Global.port)
        if status == 1:
            image = Global.client.read()
            qim = ImageQt(image)
            Global.pixmap = QPixmap.fromImage(qim)
            self.LabelStatusSaved.setText("")
            Global.StackWidgetsRects.addWidget(ui_AddBlackRectWindow())
            Global.StackWidgetsRects.setCurrentIndex(Global.StackWidgetsRects.count() - 1)
        elif status == 0:
            self.LabelStatusSaved.setText("Введен неверный логин или пароль")
        elif status == -1:
            self.LabelStatusSaved.setText("Введен неверный ip")


    def AddMask(self):
        self.LabelStatusSaved.setText("Происходит проверка параметров камеры")
        self.repaint()

        status = checkParametersCamera(Global.user, Global.passwd, Global.ip, Global.port)
        if status == 1:
            image = Global.client.read()
            qim = ImageQt(image)
            Global.pixmap = QPixmap.fromImage(qim)
            self.LabelStatusSaved.setText("")
            Global.StackWidgetsRects.addWidget(ui_AddMaskWindow())
            Global.StackWidgetsRects.setCurrentIndex(Global.StackWidgetsRects.count() - 1)
        elif status == 0:
            self.LabelStatusSaved.setText("Введен неверный логин или пароль")
        elif status == -1:
            self.LabelStatusSaved.setText("Введен неверный ip")
