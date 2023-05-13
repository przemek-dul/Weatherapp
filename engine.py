import os
import matplotlib.pyplot as plt
import datetime
import requests
import json
import urllib.request
from deep_translator import GoogleTranslator


class Engine:
    def __init__(self, town):
        self.town = town
        self.info = None
        self.no_connection = False
        self.download_data()
        self.update_data()

    def open_data(self):
        with open('data.json', 'r') as file:
            return json.load(file)

    def download_data(self):
        link = f"http://api.weatherapi.com/v1/forecast.json?key=7bfc6f3c5fec47a484d194203230505&q={self.town}&days=3&aqi=no&alerts=no"
        try:
            response = requests.get(link)
            response.raise_for_status()
            with open('data.json', 'w') as file:
                json.dump(response.json(), file)
                self.no_connection = False
        except requests.exceptions.HTTPError as e:
            if e.response.status_code >= 400:
                self.no_connection = True
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            self.no_connection = True

    def update_data(self):
        file_name = 'data.json'
        if os.path.isfile(file_name):
            mod_time = os.path.getmtime(file_name)
            mod_time = datetime.datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d-%H')
            if str(datetime.datetime.today().strftime('%Y-%m-%d-%H')) != str(mod_time):
                self.download_data()
        else:
            self.download_data()
        if not self.no_connection:
            self.info = self.open_data()

    def plot(self, day=0):
        fig, ax = plt.subplots(dpi=120)
        fig.set_facecolor('#f0f0f0')
        ax.set_facecolor("#f0f0f0")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        if self.no_connection:
            return fig
        temps = []
        dates = []
        for data in self.info['forecast']['forecastday'][day]['hour']:
            temps.append(data["temp_c"])
            dates.append(data['time'][-5:])

        ax.plot(dates, temps, c='yellow')
        ax.grid(axis='y')
        ax.set_ylabel('Temperatura [°C]')
        ax.fill_between(dates, temps, facecolor='yellow', alpha=0.45)
        ax.set_xticks(range(0, len(dates), 3))
        ax.set_xticklabels(dates[::3])
        ax.set_xlim((0, 23))
        ax.set_ylim(bottom=min(temps) - 1)

        return fig

    def get_date(self, day=0):
        if self.no_connection:
            return "bd."
        if day == 0:
            return self.info["current"]["last_updated"]
        else:
            return self.info['forecast']['forecastday'][day]["date"]

    def get_img(self, day=0):
        if self.no_connection:
            return "bd."
        if day == 0:
            url2 = str(self.info["current"]["condition"]["icon"])
        else:
            url2 = self.info['forecast']['forecastday'][day]["day"]["condition"]["icon"]
        url = "https://cdn.weatherapi.com/weather/128x128"
        i = url2.find('x64/')
        url2 = url2[i + 3::]
        url = url + url2
        data = urllib.request.urlopen(url).read()

        return data

    def get_temp(self, day=0):
        if self.no_connection:
            return "bd."
        if day == 0:
            return self.info["current"]["temp_c"]
        else:
            return self.info['forecast']['forecastday'][day]["day"]["maxtemp_c"]

    def get_wind(self, day=0):
        if self.no_connection:
            return "bd."
        if day == 0:
            return self.info["current"]["wind_kph"]
        else:
            return self.info['forecast']['forecastday'][day]["day"]["maxwind_kph"]

    def get_humidity(self, day=0):
        if self.no_connection:
            return "bd."
        if day == 0:
            return self.info["current"]["humidity"]
        else:
            return self.info['forecast']['forecastday'][day]['hour'][5]["humidity"]

    def get_pressure(self, day=0):
        if self.no_connection:
            return "bd."
        if day == 0:
            return self.info["current"]["pressure_mb"]
        else:
            return self.info['forecast']['forecastday'][day]['hour'][5]["pressure_mb"]

    def get_desc(self, day=0):
        if self.no_connection:
            return "bd."
        if day == 0:
            text = self.info["current"]["condition"]["text"]
        else:
            text = self.info['forecast']['forecastday'][day]["day"]["condition"]["text"]

        return GoogleTranslator(source='auto', target='pl').translate(text)

    def get_city(self):
        if self.no_connection:
            return "bd."
        text = self.info["location"]["name"]

        return GoogleTranslator(source='auto', target='pl').translate(text)

    def rain_plot(self, day=0):
        fig, ax = plt.subplots(dpi=120)
        fig.set_facecolor('#f0f0f0')
        ax.set_facecolor("#f0f0f0")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        if self.no_connection:
            return fig
        chances = []
        dates = []
        for data in self.info['forecast']['forecastday'][day]['hour']:
            chances.append(data["chance_of_rain"])
            dates.append(data['time'][-5:])
        for i in range(0, len(chances) - 1):
            ax.plot([dates[i], dates[i + 1]], [chances[i], chances[i]], c='blue')
            ax.fill_between([dates[i], dates[i + 1]], [chances[i], chances[i]], facecolor='blue', alpha=0.35)
        ax.grid(axis='y')
        ax.set_ylabel('Szansa opadów [%]')
        ax.set_xticks(range(0, len(dates), 3))
        ax.set_xticklabels(dates[::3])
        ax.set_xlim((0, 23))
        ax.set_ylim((-0.1, 100))

        return fig


if __name__ == "__main__":
    b = Engine("Lasdsadon")
    fig = b.rain_plot()
    plt.show()
