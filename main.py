# TODO
# цели
# задачи на день

# несколько записей
# напоминание
import csv
import sys

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
import weather

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
import weather
import registration
import Datebook


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.main_icon.resize(112, 112)
        self.logo = QPixmap('data/main_icon.jpg')
        self.main_icon.setPixmap(self.logo)
        self.centralwidget.setStyleSheet("background-color: white;")
        self.username.setStyleSheet("color: rgb(11,122,183); font-size: 14px")
        self.name.setStyleSheet("color: rgb(11,122,183); font-size: 30px")
        self.btn_login.clicked.connect(self.run)
        self.btn_login.setStyleSheet(
            "QPushButton {background-color: rgb(51,122,183); color: White; border-radius: 4px;}"
            "QPushButton:pressed {background-color:rgb(31,101,163) ; }")
        self.btn_registration.setStyleSheet("QPushButton {background-color: white; color: grey; border-radius: 0px;}"
                                            "QPushButton:pressed {background-color:rgb(31,101,163) ; }")
        self.error.setStyleSheet("color: red; font-size: 12px")
        self.btn_registration.clicked.connect(self.connect)

    def get_table(self):
        result = {}
        with open('users.csv', encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
            for i in reader:
                result[i['username']] = [i['city'], i['datebook']]
        return result

    def run(self):
        self.error.setText('')
        data_users = self.get_table()
        if self.user_answer.text() in data_users.keys():
            try:
                self.weather = weather.Weather(data_users[self.user_answer.text()][0])
                self.weather.show()
                self.datebook = Datebook.DateBook(self.user_answer.text() ,data_users[self.user_answer.text()][1])
                self.datebook.show()
            except:
                pass
        else:
            self.error.setText('incorrect login')

    def connect(self):
        self.add_user = registration.Registration()
        self.add_user.show()


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
