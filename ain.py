import os
import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QGuiApplication
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit
from useful_defs import toponyms_searcher, spn_serch

SCREEN_SIZE = [600, 550]
MAP_TYPES = ['map', 'sat', 'sat,skl']


def map_request(coords, z, map_type, marks, spn=False):
    api_server = 'https://static-maps.yandex.ru/1.x'
    if not spn:
        params = {
            'l': map_type,
            'll': ','.join([str(el) for el in coords]),
            'z': z
            } 
    else:
        params = {
            'l': map_type,
            'll': ','.join([str(el) for el in coords]),
            'z': z,
            'spn': spn,
            'pt': ','.join([str(el) for el in marks])
            }    
    response = requests.get(api_server, params=params)
    return response


class Main_window(QWidget):
    def __init__(self):
        super().__init__()
        self.map = 'map.png'
        self.map_type = 0
        self.z = 8
        self.mark = 0
        self.initUI()

    def getImage(self):
        try:
            self.coords = [float(el) for el in self.input.text().split()]
            if self.mark:
                map_resp = map_request(self.coords, self.z, MAP_TYPES[self.map_type], self.mark)
            else:
                map_resp = map_request(self.coords, self.z, MAP_TYPES[self.map_type], self.coords)

        except:
            self.coords = self.input.text()
            response = toponyms_searcher(self.coords)
            need_city = response["response"]["GeoObjectCollection"]["featureMember"][0]
            need_coord = need_city['Point']['pos'].split()
            self.coords = need_coord
            self.mark = need_coord
            spn = spn_serch(need_city)
            map_resp = map_request(self.coords, self.z, MAP_TYPES[self.map_type], self.mark, spn=spn)
            

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
            
            elif e.key() in (Qt.Key_PageUp, Qt.Key_PageDown, Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right, Qt.Key_L):
                print(e.key(), Qt.Key_PageUp, Qt.Key_PageDown, Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right, Qt.Key_L)
                if e.key() == Qt.Key_PageUp:
                    if self.z < 17:
                        self.z += 1

                elif e.key() == Qt.Key_PageDown:
                    if self.z > 0:
                        self.z -= 1
                
                elif e.key() == Qt.Key_Up:
                    if self.coords[1] < 90:
                        self.coords[1] += 0.03 * (18 - self.z)
                
                elif e.key() == Qt.Key_Down:
                    if self.coords[1] > -90:
                        self.coords[1] -= 0.03 * (18 - self.z)
                    
                elif e.key() == Qt.Key_Left:
                    if self.coords[0] > -180:
                        self.coords[0] -= 0.03 * (18 - self.z)
                
                elif e.key() == Qt.Key_Right:
                    if self.coords[0] < 180:
                        self.coords[0] += 0.03 * (18 - self.z)
                
                elif e.key() == Qt.Key_L:
                        self.map_type = (self.map_type + 1) % 3

                
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