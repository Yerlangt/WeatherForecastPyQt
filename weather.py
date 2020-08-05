import datetime
from PyQt5 import QtCore
import sys
import requests
import pyowm
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

APPID = "19ed723472e40423140d8b1bc89e8711"  # app key to pyowm
decoder_icon = {'Clouds': '7.png',
                'Mist': '8.png',
                'Smoke': '8.png',
                'few clouds': '2.png',
                'Rain': '3.png',
                'Snow': '5.png',
                'Clear': '1.png',
                'Fog': '8.png'}
weekday = {
    '0': 'MON',
    '1': 'TUE',
    '2': 'WED',
    '3': 'THU',
    '4': 'FRI',
    '5': 'SAT',
    '6': 'SUN',
}


class Weather(QWidget):
    def __init__(self, city):
        super().__init__()
        self.city = city
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 400, 400, 400)
        self.setWindowTitle('Weather forecast')
        self.move(230, 160)
        # текущая погода в опреденном
        weather_request = self.get_weather(APPID, self.city)

        self.current_datetime = datetime.datetime.now()  # текущее время
        self.now = self.current_datetime.timetuple()  # текущее время в формате tuple
        self.forecast = self.get_forecast(self.now.tm_mday)  # прогноз погоды на следующую неделю
        # установка разного заднего фона в зависимости от времени
        if 18 <= self.current_datetime.hour <= 24 or 0 <= self.current_datetime.hour <= 6:
            self.day_or_night = QPixmap('data/time/night.jpg')
        else:
            self.day_or_night = QPixmap('data/time/day.jpg')

        self.bground = QLabel(self)
        self.bground.setPixmap(self.day_or_night)
        # установка значка погоды
        self.icon = QLabel(self)
        self.icon.move(50, 20)
        self.status = QPixmap('data/weather signs/' + decoder_icon[
            weather_request.get_status()])  # определенный значок в зависимости от прогноза погоды
        self.icon.setPixmap(self.status)
        # детальный статус погоды
        self.detailed_status = QLabel(self)
        self.detailed_status.resize(170, 22)
        self.detailed_status.move(30, 155)
        self.detailed_status.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.detailed_status.setAlignment(Qt.AlignCenter)
        self.detailed_status.setText(str(weather_request.get_detailed_status()).capitalize())
        self.detailed_status.setStyleSheet("""
            font-size: 22px;
            color: white;
        """)
        # Текущий город
        self.location = QLabel(self)
        self.location.setText(self.city)
        self.location.resize(170, 22)
        self.location.move(30, 185)
        self.location.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.location.setAlignment(Qt.AlignCenter)
        self.location.setStyleSheet("""
                    font-size: 22px;
                    color: white;
                """)
        # текущая температура
        self.tempreture = QLabel(self)
        self.tempreture.move(220, 15)
        self.tempreture.setText(str(int(weather_request.get_temperature('celsius')['temp'])) + '°')
        self.tempreture.setStyleSheet("""
                    font-size: 90px;
                    color: white;
                """)
        # Расположение текущего часа и минуты
        self.time = QLabel(self)
        self.time.move(240, 135)
        self.time.setText(str(self.now.tm_hour).rjust(2, '0') + ':' + str(self.now.tm_min).rjust(2, '0'))
        self.time.setStyleSheet("""
                            font-size: 50px;
                            color: white;
                        """)
        # создание timer, который каждые 60 секунд изменяет минуты
        self.i = self.now.tm_sec
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(1000)

        # создание следущего дня, температуры и значка погоды
        self.second_day = QLabel(self)
        self.second_day.move(65, 230)
        self.second_day.setText(weekday[str((self.now.tm_wday + 1) % 7)])
        self.second_day.setStyleSheet("""
                                            font-size: 20px;
                                            color: white;
                                        """)

        self.second_day_temp = QLabel(self)

        self.second_day_temp.move(60, 310)
        self.second_day_temp.setText(str(int(self.forecast[0]['main']['temp'])) + '°')

        self.second_day_temp.setStyleSheet("""
                                                    font-size: 15px;
                                                    color: white;
                                                """)
        self.second_night_temp = QLabel(self)
        self.second_night_temp.setText(str(int(self.forecast[1]['main']['temp'])) + '°')
        self.second_night_temp.move(85, 310)
        self.second_night_temp.setStyleSheet("""
                                                            font-size: 15px;
                                                            color: grey;
                                                        """)
        self.second_day_icon = QLabel(self)
        a = self.forecast[0]['weather'][0]['main']

        self.second_day_status = QPixmap('data/mini weather signs/' + decoder_icon[a])
        self.second_day_icon.setPixmap(self.second_day_status)
        self.second_day_icon.move(70, 275)

        self.third_day = QLabel(self)
        self.third_day.move(190, 230)
        self.third_day.setText(weekday[str((self.now.tm_wday + 2) % 7)])
        self.third_day.setStyleSheet("""
                                            font-size: 20px;
                                            color: white;
                                        """)
        self.third_day_temp = QLabel(self)

        self.third_day_temp.move(185, 310)
        self.third_day_temp.setText(str(int(self.forecast[2]['main']['temp'])) + '°')

        self.third_day_temp.setStyleSheet("""
                                                            font-size: 15px;
                                                            color: white;
                                                        """)
        self.third_night_temp = QLabel(self)
        self.third_night_temp.setText(str(int(self.forecast[3]['main']['temp'])) + '°')
        self.third_night_temp.move(210, 310)
        self.third_night_temp.setStyleSheet("""
                                                                    font-size: 15px;
                                                                    color: grey;
                                                                """)
        self.third_day_icon = QLabel(self)
        a = self.forecast[2]['weather'][0]['main']

        self.third_day_status = QPixmap('data/mini weather signs/' + decoder_icon[a])
        self.third_day_icon.setPixmap(self.third_day_status)
        self.third_day_icon.move(200, 275)

        self.forth_day = QLabel(self)
        self.forth_day.move(315, 230)
        self.forth_day.setText(weekday[str((self.now.tm_wday + 3) % 7)])
        self.forth_day.setStyleSheet("""
                                            font-size: 20px;
                                            color: white;
                                        """)
        self.forth_day_temp = QLabel(self)

        self.forth_day_temp.move(310, 310)
        self.forth_day_temp.setText(str(int(self.forecast[4]['main']['temp'])) + '°')

        self.forth_day_temp.setStyleSheet("""
                                                                    font-size: 15px;
                                                                    color: white;
                                                                """)
        self.forth_night_temp = QLabel(self)
        self.forth_night_temp.setText(str(int(self.forecast[5]['main']['temp'])) + '°')
        self.forth_night_temp.move(335, 310)
        self.forth_night_temp.setStyleSheet("""
                                                                            font-size: 15px;
                                                                            color: grey;
                                                                        """)
        self.forth_day_icon = QLabel(self)
        a = self.forecast[4]['weather'][0]['main']

        self.forth_day_status = QPixmap('data/mini weather signs/' + decoder_icon[a])
        self.forth_day_icon.setPixmap(self.forth_day_status)
        self.forth_day_icon.move(325, 275)

    def get_forecast(self, m_day):
        # создание запроса и получение прогноза на след 3 дня с сайта opm.org
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'q': self.city, 'units': 'metric', 'lang': 'ru', 'APPID': APPID})
        need_data = [m_day, m_day + 1, m_day + 2, m_day + 3]
        result = []
        data = res.json()
        for i in data['list']:
            data_time = i['dt_txt'].split(' ')
            data = data_time[0].split('-')
            time = data_time[1].split(':')
            if int(data[2]) in need_data and (time[0] == '03' or time[0] == '15'):
                result.append(i)
        return result

    def tick(self):
        # динамическое обновление часов
        self.i += 1
        if self.i == 59:
            update_time = datetime.datetime.now().timetuple()
            self.time.setText(str(update_time.tm_hour).rjust(2, '0') + ':' + str(update_time.tm_min).rjust(2, '0'))
            self.i = 0

    def get_weather(self, appid, city):
        # Search for current weather in current city
        owm = pyowm.OWM(appid)
        observation = owm.weather_at_place(city)
        w = observation.get_weather()

        return w  # <Weather - reference status, time=2019-12-18 09:20
