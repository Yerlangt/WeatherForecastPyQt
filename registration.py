import csv
import sys

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow


class Registration(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('reg.ui', self)
        self.main_icon.resize(112, 112)
        self.logo = QPixmap('data/main_icon.jpg')
        self.main_icon.setPixmap(self.logo)
        # self.centralwidget.setStyleSheet("background-color: white;")
        self.name.setStyleSheet("color: rgb(11,122,183); font-size: 30px")

        self.username.setStyleSheet("color: rgb(11,122,183); font-size: 14px")
        self.city.setStyleSheet("color: rgb(11,122,183); font-size: 14px")
        self.confirm_btn.setStyleSheet(
            "QPushButton {background-color: rgb(51,122,183); color: White; border-radius: 4px;}"
            "QPushButton:pressed {background-color:rgb(31,101,163) ; }")
        self.confirm_btn.clicked.connect(self.set_table)

    def set_table(self):
        with open('users.csv', encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
            for i in reader:
                num = i['id']

        with open('users.csv', 'a', newline='') as csvfile:

            writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            n,otes = 'Notes:'
            writer.writerow([str(int(num) + 1), self.username_answer.text(), self.city_answer.text(), notes])
            self.result.setText('successfully')
            self.result.setStyleSheet("color: LimeGreen	; font-size: 12px")
            self.username_answer.setText('')
            self.city_answer.setText('')

