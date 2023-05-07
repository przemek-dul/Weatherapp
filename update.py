import requests
import random
import time

data = {
    "temperature": 20.5,
    "pressure": 1000.0
}
while True:
    data["temperature"] = random.randint(10, 30)
    data["pressure"] = random.randint(900, 1100)
    response = requests.put("http://127.0.0.1:8000/update_town/krakow", json=data)
    time.sleep(0.5)

