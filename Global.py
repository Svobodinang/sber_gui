from PyQt5 import QtCore, QtGui, QtWidgets
import os
import json

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

def getfilesJsonInPath(path):
    # Массив всех файлов в папке
    filesInPath = [f for f in os.listdir(path)]
    filesJsonInPath = []
    for file in filesInPath:
        # Проверяем, чтобы расширение было .json и название содержало слово camera
        if os.path.splitext(file)[1] == '.json' and os.path.splitext(file)[0][0:6] == 'camera':
            filesJsonInPath.append(file)
    return filesJsonInPath


class Global:
    StackWidgets = QtWidgets.QStackedLayout()
    StackWidgetsRects = QtWidgets.QStackedLayout()

    data = readDataFromJson('./paths.json')
    pathData = data['data']
    pathCamera = pathData + "/camera/"
    pathCore = pathData + "/core/core.json"
    pathLogs = ""

    print(pathCamera)
    print(pathCore)

    idCamerasQtArr = {}
    idCamerasArrQt = {}
    arrWhiteRects = {
        1: [],
        2: [],
        3: [],
        4: []
    }
    arrBlackRects = {
        1: [],
        2: [],
        3: [],
        4: []
    }
    arrMask = {
        1: [],
        2: [],
        3: [],
        4: []
    }

    Window_width = 840
    Window_heigth = 540


    ButtonBackText = '\u2190'
    ButtonBackGeometryL = 10
    ButtonBackGeometryT = 10
    ButtonBackGeometryW = 50
    ButtonBackGeometryH = 50

    # Получаем количество файлов json в папке с камерами
    countCameras = len(getfilesJsonInPath(pathCamera))
    numCamera = 0
    ip = ""
    user = ""
    passwd = ""
    port = ""
    pixmap = 0
    client = 0

    dataCameraEmpty = {
        "ip": "",
        "port": "",
        "user": "",
        "password": "",
        "rects_white": [],
        "rects_black": [],
        "mask": []
    }

    dataCoreCameraEmpty = {
            "name": "",
            "config_path": "",
            "fp_white": "detectors/fp_white.json",
            "fp_black": "detectors/fp_black.json"
    }
