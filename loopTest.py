import os
import matplotlib.pyplot as plt
import datetime
import requests
import json
import numpy as np


def open_data():
    with open('data.json', 'r') as file:
        return json.load(file)


def download_data():
    link = "http://api.weatherapi.com/v1/forecast.json?key=7bfc6f3c5fec47a484d194203230505&q=Tarnobrzeg&days=1&aqi=no&alerts=no"
    response = requests.get(link)
    with open('data.json', 'w') as file:
        json.dump(response.json(), file)


def update_data():
    file_name = 'data.json'
    if os.path.isfile(file_name):
        mod_time = os.path.getmtime(file_name)
        mod_time = datetime.datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d-%H')
        if str(datetime.datetime.today().strftime('%Y-%m-%d-%H')) != str(mod_time):
            download_data()
    else:
        download_data()


update_data()
city_info = open_data()
temps = []
dates = []
for data in city_info['forecast']['forecastday'][0]['hour']:
    temps.append(data["temp_c"])
    dates.append(data['time'][-5:])

temp = city_info["current"]["temp_c"]
city = city_info["location"]["name"]
date = city_info["current"]["last_updated"]
title = f"{temp}°C   |   {city}: {date}"

fig, ax = plt.subplots()
ax.plot(dates, temps, c='yellow')
ax.grid(axis='y')
ax.set_title(title)
ax.set_ylabel('Temperatura[°C]')
ax.set_xlabel('Godzina')
ax.fill_between(dates, temps, facecolor='yellow', alpha=0.2)
ax.set_xticks(range(0, len(dates), 3))
ax.set_xticklabels(dates[::3], rotation=45)
ax.set_xlim((0, 23))
ax.set_ylim(bottom=min(temps)-1)
plt.show()
