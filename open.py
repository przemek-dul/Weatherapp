import requests
import matplotlib.pyplot as plt
import time
from matplotlib.animation import FuncAnimation

class Que:
    def __init__(self, max_size=100):
        self.data = []
        self.max_size = max_size

    def add(self, value):
        self.data.append(value)
        if len(self.data) > self.max_size:
            self.data.pop(0)

    def get_data(self):
        return self.data


temp = Que()
press = Que()

fig, ax = plt.subplots()


def animate(i):
    response = requests.get("http://127.0.0.1:8000/town/krakow")
    data = response.json()
    temp.add(data["temperature"])
    press.add(data["pressure"])
    ax.clear()
    ax.grid()
    ax.plot(temp.get_data())


ani = FuncAnimation(fig, animate, frames=20, interval=100, repeat=True)
plt.show()