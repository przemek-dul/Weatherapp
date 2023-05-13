import PyQt5.QtWidgets as wg
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from engine import Engine
import matplotlib.pyplot as plt
import json
import os
from deep_translator import GoogleTranslator


class Figure(FigureCanvas):
    def __init__(self, parent=None, fig=None):
        self.fig = fig or plt.figure(figsize=(2, 1))
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)


class App(wg.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(765, 600)
        self.setWindowTitle("Pogoda")
        self.setWindowIcon(QIcon("ikona.png"))
        self.info_style = "font-size: 13px;color: #696969"
        self.day_btn_size = ((self.width() - 20) // 3, 100)
        self.engine = None
        self.read_last_city()
        self.day = 0
        self.curr_polt = "temp"
        self.initUI()


    def initUI(self):
        self.today_btn = wg.QPushButton(self)
        self.today_btn.resize(self.day_btn_size[0], self.day_btn_size[1])
        self.today_btn.move(5, self.height() - self.today_btn.height() - 5)
        self.today_btn.setText("Dzisiaj")
        self.today_btn.setStyleSheet(self.set_style_to_btn("#006400"))
        self.today_btn.clicked.connect(self.click_today)

        self.tomorrow_btn = wg.QPushButton(self)
        self.tomorrow_btn.resize(self.day_btn_size[0], self.day_btn_size[1])
        self.tomorrow_btn.move(10 + self.day_btn_size[0], self.height() - self.today_btn.height() - 5)
        self.tomorrow_btn.setText("Jutro")
        self.tomorrow_btn.setStyleSheet(self.set_style_to_btn("#4CAF50"))
        self.tomorrow_btn.clicked.connect(self.click_tomorrow)

        self.a_tomorrow_btn = wg.QPushButton(self)
        self.a_tomorrow_btn.resize(self.day_btn_size[0], self.day_btn_size[1])
        self.a_tomorrow_btn.move(15 + 2 * self.day_btn_size[0], self.height() - self.today_btn.height() - 5)
        self.a_tomorrow_btn.setText("Pojutrze")
        self.a_tomorrow_btn.setStyleSheet(self.set_style_to_btn("#4CAF50"))
        self.a_tomorrow_btn.clicked.connect(self.click_a_tomorrow)

        self.day_info = wg.QGroupBox(self)
        self.day_info.resize((self.width() - 20) // 2, 150)
        self.day_info.setStyleSheet("QGroupBox { border: 0; }")

        self.weather_img = wg.QLabel(self.day_info)
        self.weather_img.resize(128, 128)
        self.set_img(self.day)

        self.temp_info = wg.QLabel(self.day_info)
        self.temp_info.resize(110, 100)
        self.temp_info.move(self.weather_img.width(), self.day_info.height() // 2 - self.temp_info.height() // 2)
        self.temp_info.setStyleSheet("text-decoration: none;display: inline-block;font-size: 32px;")
        self.temp_info.setText(f"{self.engine.get_temp()} °C")

        self.rhw_box = wg.QGroupBox(self.day_info)
        self.rhw_box.setStyleSheet("QGroupBox { border: none; }")
        self.rhw_box.resize(125, 50)
        self.rhw_box.move(self.temp_info.x() + self.temp_info.width() + 5,
                          self.day_info.height() // 2 - self.rhw_box.height() // 2)

        self.rain_info = wg.QLabel(self.rhw_box)
        self.rain_info.setText(f"ciśnienie: {self.engine.get_pressure()} hPa")
        self.rain_info.move(0, 0)
        self.rain_info.setStyleSheet(self.info_style)

        self.humidity_info = wg.QLabel(self.rhw_box)
        self.humidity_info.setText(f"wilgotność: {self.engine.get_humidity()} %")
        self.humidity_info.move(0, 15)
        self.humidity_info.setStyleSheet(self.info_style)

        self.wind_info = wg.QLabel(self.rhw_box)
        self.wind_info.setText(f"wiatr: {self.engine.get_wind()} km/h")
        self.wind_info.move(0, 30)
        self.wind_info.setStyleSheet(self.info_style)

        self.city_day_info = wg.QGroupBox(self)
        self.city_day_info.resize((self.width() - 20) // 2, 150)
        self.city_day_info.setStyleSheet("QGroupBox { border: 0; }")
        self.city_day_info.move(self.day_info.width() + 20, 0)

        self.city = wg.QLabel(self.city_day_info)
        self.city.resize(self.city_day_info.width() - 15, self.city_day_info.height())
        self.city.move(0, 30)
        self.city.setStyleSheet("font-size: 24px;")
        self.city.setAlignment(Qt.AlignRight)
        self.city.setText(f"{self.engine.get_city()}")

        self.date = wg.QLabel(self.city_day_info)
        self.date.resize(self.city_day_info.width() - 15, self.city_day_info.height())
        self.date.move(0, 60)
        self.date.setStyleSheet("font-size: 18px;color: #696969")
        self.date.setAlignment(Qt.AlignRight)
        self.date.setText(f"{self.engine.get_date()}")

        self.weather_desc = wg.QLabel(self.city_day_info)
        self.weather_desc.resize(self.city_day_info.width() - 15, self.city_day_info.height())
        self.weather_desc.move(0, 80)
        self.weather_desc.setStyleSheet("font-size: 18px;color: #696969")
        self.weather_desc.setAlignment(Qt.AlignRight)
        self.weather_desc.setText(self.engine.get_desc())

        self.my_canvas = Figure(fig=self.engine.plot())

        self.plot_container = wg.QGroupBox(self)
        self.plot_container.resize(self.width(), self.width() - self.day_btn_size[0] - self.day_info.height())
        self.plot_container.move(0, self.day_info.height() - 30)

        self.plot_container_layout = wg.QHBoxLayout()
        self.plot_container_layout.addWidget(self.my_canvas)

        self.plot_container.setLayout(self.plot_container_layout)
        self.plot_container.setStyleSheet("QGroupBox { border: 0; }")

        self.town_finder_box = wg.QGroupBox(self)
        self.town_finder_box.resize(400, 60)
        self.town_finder_box.move(40, 115)
        self.town_finder_box.setStyleSheet("QGroupBox { border: 0; }")

        self.town_text = wg.QLabel(self.town_finder_box)
        self.town_text.setText("Miejscowość: ")
        self.town_text.setStyleSheet("font-size: 18px;")
        self.town_text.move(0, 5)

        self.input_town = wg.QLineEdit(self.town_finder_box)
        self.input_town.setStyleSheet("font-size: 18px;color: #696969")
        self.input_town.move(self.town_text.width() + 5, 0)
        self.input_town.resize(200, 30)
        self.input_town.setText(self.engine.get_city())
        self.input_town.setAlignment(Qt.AlignRight)

        self.input_btn = wg.QPushButton(self.town_finder_box)
        self.input_btn.move(self.town_text.width() + self.input_town.width() + 10, 0)
        self.input_btn.resize(80, 30)
        self.input_btn.setText("Zatwierdz")
        self.input_btn.setStyleSheet("background-color: #4CAF50; border: none;color: white; font-size: 15px;")
        self.input_btn.clicked.connect(self.new_town)

        self.select_temp_plot_btn = wg.QPushButton(self)
        self.select_temp_plot_btn.move(450, 135)
        self.select_temp_plot_btn.setText("Temperatura")
        self.select_temp_plot_btn.resize(100, 30)
        self.select_temp_plot_btn.setStyleSheet(self.set_style_to_select_btn(True))
        self.select_temp_plot_btn.clicked.connect(self.temp_clicked)

        self.select_rain_plot_btn = wg.QPushButton(self)
        self.select_rain_plot_btn.move(560, 135)
        self.select_rain_plot_btn.setText("Opady")
        self.select_rain_plot_btn.resize(100, 30)
        self.select_rain_plot_btn.setStyleSheet(self.set_style_to_select_btn())
        self.select_rain_plot_btn.clicked.connect(self.rain_clicked)

    def rain_clicked(self):
        self.select_temp_plot_btn.setStyleSheet(self.set_style_to_select_btn(False))
        self.select_rain_plot_btn.setStyleSheet(self.set_style_to_select_btn(True))

        self.plot_container_layout.removeWidget(self.my_canvas)
        self.my_canvas.deleteLater()
        plt.close('all')
        self.my_canvas = Figure(fig=self.engine.rain_plot(self.day))
        self.plot_container_layout.addWidget(self.my_canvas)
        self.curr_polt = "rain"

    def temp_clicked(self):
        self.select_temp_plot_btn.setStyleSheet(self.set_style_to_select_btn(True))
        self.select_rain_plot_btn.setStyleSheet(self.set_style_to_select_btn(False))

        self.plot_container_layout.removeWidget(self.my_canvas)
        self.my_canvas.deleteLater()
        plt.close('all')
        self.my_canvas = Figure(fig=self.engine.plot(self.day))
        self.plot_container_layout.addWidget(self.my_canvas)
        self.curr_polt = "temp"

    def set_img(self, day):
        data = self.engine.get_img(day)
        if data != "bd.":
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            pixmap = pixmap.scaled(self.weather_img.height(), self.weather_img.height())
            self.weather_img.setPixmap(pixmap)

    def set_style_to_btn(self, color):
        return f"background-color: {color}; border: none;color: white;padding: 15px " \
               "32px;text-align: center;text-decoration: none;display: inline-block;font-size: 21px;"

    def set_style_to_select_btn(self, primary=False):
        if primary:
            return f"background-color: #f0f0f0; border: none;color: black;text-align: center;text-decoration: " \
               f"none;font-size: 15px;border-bottom: 3px solid orange; "
        else:
            return f"background-color: #f0f0f0; border: none;color: black;text-align: center;text-decoration: " \
                   f"none;font-size: 15px"

    def new_town(self):
        inp = self.input_town.text()
        inp = GoogleTranslator(source='pl', target='en').translate(inp)
        self.engine.town = inp
        self.engine.download_data()
        self.engine.update_data()
        self.click_today()

    def update_data(self):
        self.temp_info.setText(f"{self.engine.get_temp(self.day)} °C")
        self.rain_info.setText(f"ciśnienie: {self.engine.get_pressure(self.day)} hPa")
        self.humidity_info.setText(f"wilgotność: {self.engine.get_humidity(self.day)} %")
        self.wind_info.setText(f"wiatr: {self.engine.get_wind(self.day)} km/h")
        self.city.setText(f"{self.engine.get_city()}")
        self.date.setText(f"{self.engine.get_date(self.day)}")
        self.weather_desc.setText(self.engine.get_desc(self.day))
        self.set_img(self.day)

        self.plot_container_layout.removeWidget(self.my_canvas)
        self.my_canvas.deleteLater()
        plt.close('all')
        if self.curr_polt == "temp":
            self.my_canvas = Figure(fig=self.engine.plot(self.day))
        else:
            self.my_canvas = Figure(fig=self.engine.rain_plot(self.day))
        self.plot_container_layout.addWidget(self.my_canvas)

    def click_tomorrow(self):
        self.tomorrow_btn.setStyleSheet(self.set_style_to_btn("#006400"))
        self.today_btn.setStyleSheet(self.set_style_to_btn("#4CAF50"))
        self.a_tomorrow_btn.setStyleSheet(self.set_style_to_btn("#4CAF50"))

        self.day = 1
        self.update_data()

    def click_today(self):
        self.tomorrow_btn.setStyleSheet(self.set_style_to_btn("#4CAF50"))
        self.today_btn.setStyleSheet(self.set_style_to_btn("#006400"))
        self.a_tomorrow_btn.setStyleSheet(self.set_style_to_btn("#4CAF50"))

        self.day = 0
        self.update_data()

    def click_a_tomorrow(self):
        self.tomorrow_btn.setStyleSheet(self.set_style_to_btn("#4CAF50"))
        self.today_btn.setStyleSheet(self.set_style_to_btn("#4CAF50"))
        self.a_tomorrow_btn.setStyleSheet(self.set_style_to_btn("#006400"))

        self.day = 2
        self.update_data()

    def read_last_city(self):
        file_name = 'city.json'
        if os.path.isfile(file_name):
            with open(file_name, 'r') as file:
                data = json.load(file)
                city = data["city"]
                self.engine = Engine(city)
        else:
            self.engine = Engine("London")


def save_last_city():
    data = {"city": a.engine.get_city()}
    with open('city.json', "w") as file:
        json.dump(data, file)


if __name__ == "__main__":
    app = wg.QApplication(sys.argv)
    a = App()
    a.show()
    app.aboutToQuit.connect(save_last_city)
    sys.exit(app.exec())

