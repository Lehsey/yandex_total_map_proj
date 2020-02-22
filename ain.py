import os
import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit


SCREEN_SIZE = [600, 550]


def map_request(coords):
    api_server = 'https://static-maps.yandex.ru/1.x'
    params = {
        'l': 'map',
        'll': coords,
        'z': 8
    }
    response = requests.get(api_server, params=params)
    return response


class Main_window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def getImage(self):
        coords = ','.join(self.input.text().split())
        map_resp = map_request(coords)
        if not requests:
            print(map_resp)
            sys.exit(1)

        self.map = 'map.png'
        with open(self.map, 'wb') as file:
            file.write(map_resp.content)
        self.pixmap = QPixmap(self.map)
        self.image.setPixmap(self.pixmap)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setFixedSize(*SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.input_info = QLabel(self)
        self.input_info.setText("Введите Информацию")
        self.input_info.move(80, 520)
        self.input = QLineEdit(self)
        self.input.setFixedSize(300, 20)
        self.input.move(200, 520)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.getImage()

    def closeEvent(self, event):
        os.remove(self.map)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_window()
    ex.show()
    sys.exit(app.exec())