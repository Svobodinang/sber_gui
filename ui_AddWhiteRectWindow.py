from PyQt5 import QtCore, QtGui, QtWidgets
from Global import Global
import json
import os.path


# Класс квадрата, переопределен цвет и ширина границ
class MyRect(QtWidgets.QGraphicsRectItem):
    def __init__(self, rectang, *args, **kwargs):
        QtWidgets.QGraphicsRectItem.__init__(self, rectang, *args, **kwargs)
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable |
                      QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)

        self.pen = QtGui.QPen(QtCore.Qt.darkGreen)
        self.pen.setWidth(2)
        self.startX = self.sceneBoundingRect().x()
        self.setPen(self.pen)


class ui_AddWhiteRectWindow(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(QtWidgets.QWidget, self).__init__(parent)
        self.setupUi()
        self.init_gui()

    def setupUi(self):
        self.resize(Global.Window_width, 600)

        # Кнопка добавления квадратика
        self.PushButtonAddRect = QtWidgets.QPushButton(self)
        self.PushButtonAddRect.setText('Добавить область')
        self.PushButtonAddRect.setFixedSize(Global.Window_width, 35)

        # Кнопка сохранения квадратиков
        self.PushButtonSave = QtWidgets.QPushButton(self)
        self.PushButtonSave.setText('Сохранить')
        self.PushButtonSave.setFixedSize(Global.Window_width, 35)

        # Кнопка удаления последнего квадратика
        self.PushButtonDeleteLast = QtWidgets.QPushButton(self)
        self.PushButtonDeleteLast.setText('Удалить')
        self.PushButtonDeleteLast.setFixedSize(Global.Window_width, 35)

        self.pathCamera = Global.pathCamera + "camera" + str(Global.numCamera) + ".json"

        # Изображение с камеры
        self.pixmap = Global.pixmap
        self.pixmap = self.pixmap.scaledToWidth(768)
        # 0.4 - коэффициент!

        # Сигналы
        self.PushButtonAddRect.clicked.connect(self.addRect)
        self.PushButtonSave.clicked.connect(self.save)
        self.PushButtonDeleteLast.clicked.connect(self.deleteLast)

        # Сцена для отображения всего
        self.scene = QtWidgets.QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 768, 435)
        self.scene.addPixmap(self.pixmap)
        # Создаем view для отображения сцены
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setGeometry(0, 0, 768, 435)
        # Убираем скорллбар
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # Cоздаем таблицу, в которую можно добалять кнопки сцену
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        # Добавляем туда содержимое(кнопки, view со сценой)
        self.layout.addWidget(self.view)
        self.layout.addWidget(self.PushButtonAddRect)
        self.layout.addWidget(self.PushButtonSave)
        self.layout.addWidget(self.PushButtonDeleteLast)

        # Добавляем квадратики из файла на сцену и в глобальный массив
        self.addRectsFromJsonToScene()

    def init_gui(self):
        self.setStyleSheet(open("style.qss", "r").read())

    # Метод добавления квадратиков из файла на сцену и в глобальный массив действующей камеры
    def addRectsFromJsonToScene(self):
        # Обнуляем глобальный массив
        Global.arrWhiteRects = {
            1: [],
            2: [],
            3: [],
            4: []
        }
        # Проверяем есть ли файл с настройками для данной камеры
        if os.path.exists(self.pathCamera):
            # Проверяем не пустой ли он
            if os.path.getsize(self.pathCamera) > 0:
                # Открываем
                with open(self.pathCamera, "r") as read_file:
                    data = json.load(read_file)
                    # Если в json есть поле с квадратиками
                    if 'rects_white' in data:
                        for rect in data['rects_white']:
                            rect_item = MyRect(QtCore.QRectF(rect[0] * 0.4, rect[1] * 0.4,
                                                             rect[2] * 0.4, rect[2] * 0.4))
                            # Добавляем на сцену
                            self.scene.addItem(rect_item)
                            # Добавляем в глобальный массив
                            Global.arrWhiteRects[int(Global.numCamera)].append(rect_item)

    def addRect(self):
        self.PushButtonSave.setText("Сохранить")
        self.repaint()
        # Создаем квадратик
        rect_item = MyRect(QtCore.QRectF(0, 0, 108, 108))
        # Добавляем его в глобальный массив для действующей камеры
        Global.arrWhiteRects[int(Global.numCamera)].append(rect_item)
        # Добавляем квадратик на сцену
        self.scene.addItem(rect_item)

    def deleteLast(self):
        numCamera = int(Global.numCamera)
        # Проверяем если глобальный массив с квадратиками для открытой камеры не пустой
        if len(Global.arrWhiteRects[numCamera]) > 0:
            # Удаляем со сцены(последний)
            self.scene.removeItem(Global.arrWhiteRects[numCamera][len(Global.arrWhiteRects[numCamera]) - 1])
            # Удаляем из массива(последний)
            del Global.arrWhiteRects[numCamera][len(Global.arrWhiteRects[numCamera]) - 1]

    # Метод преобразования координат квадратиков и добавляния их в словарь
    def addRectsToData(self, data):
        # Проходимся по массиву квадратиков для открытой камеры
        for rect in Global.arrWhiteRects[int(Global.numCamera)]:
            # Создаем массив с координами
            arrRectRoi = []
            # Умножаем на коэффициент
            arrRectRoi.append(round(rect.sceneBoundingRect().x() * 2.5))
            arrRectRoi.append(round(rect.sceneBoundingRect().y() * 2.5))
            arrRectRoi.append(270)
            arrRectRoi.append(270)
            # Добавляем в исходный словарь
            data['rects_white'].append(arrRectRoi)
        return data

    def save(self):
        # Проверяем есть ли файл с настройками для данной камеры
        if os.path.exists(self.pathCamera):
            # Проверяем не пустой ли он
            if os.path.getsize(self.pathCamera) > 0:
                # Открываем
                with open(self.pathCamera, "r") as read_file:
                    data = json.load(read_file)

                    # Меняем поле с координатами квадратиков, так как те квадратики, которые были в файле
                    # уже добавлены в глобальный массив, поле следует сначала занулить
                    data['rects_white'] = []
                    data = self.addRectsToData(data)

                    # Записываем в файл обновленные данные
                    with open(self.pathCamera, "w") as write_file:
                        json.dump(data, write_file)
        self.PushButtonSave.setText("Сохранено!")
        self.repaint()
