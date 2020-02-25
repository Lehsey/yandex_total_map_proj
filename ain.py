import os
import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QGuiApplication
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit


SCREEN_SIZE = [600, 550]


def map_request(coords, z):
    api_server = 'https://static-maps.yandex.ru/1.x'
    params = {
        'l': 'map',
        'll': ','.join([str(el) for el in coords]),
        'z': z
    }
    response = requests.get(api_server, params=params)
    return response


class Main_window(QWidget):
    def __init__(self):
        super().__init__()
        self.map = 'map.png'
        self.z = 8
        self.initUI()

    def getImage(self):
        self.coords = [float(el) for el in self.input.text().split()]
        map_resp = map_request(self.coords, self.z)
        if not requests:
            print(map_resp)
            sys.exit(1)

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
        self.input_info.move(65, 520)
        self.input = QLineEdit(self)
        self.input.setFixedSize(300, 20)
        self.input.move(200, 520)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)

    def keyPressEvent(self, e):
        try:
            if e.key() == Qt.Key_Return:
                self.getImage()
                self.input.clearFocus()
            
            elif e.key() in (Qt.Key_PageUp, Qt.Key_PageDown) or (Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right):
                if e.key() == Qt.Key_PageUp:
                    if self.z < 17:
                        self.z += 1

                elif e.key() == Qt.Key_PageDown:
                    if self.z > 0:
                        self.z -= 1
                
                elif e.key() == Qt.Key_Up:
                    self.coords[1] += 0.03 * (18 - self.z)
                
                elif e.key() == Qt.Key_Down:
                    self.coords[1] -= 0.03 * (18 - self.z)
                    
                elif e.key() == Qt.Key_Left:
                    self.coords[0] -= 0.03 * (18 - self.z)
                
                elif e.key() == Qt.Key_Right:
                    self.coords[0] += 0.03 * (18 - self.z)
                
                self.input.setText(' '.join([str(el) for el in self.coords]))
                self.getImage()
        except:
            pass



    def closeEvent(self, event):
        try:
            os.remove(self.map)
        except:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_window()
    ex.show()
    sys.exit(app.exec())