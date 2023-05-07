import random
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    temperature: float
    pressure: float

temp_krk = random.randint(5, 32)
pres_krk = random.randint(900, 1100)

temp_tbg = random.randint(5, 32)
pres_tbg = random.randint(900, 1100)

data = {"krakow":
    {
        "temperature": temp_krk,
        "pressure": pres_krk
    },
    "tarnobrzeg":
        {
            "temperature": temp_tbg,
            "pressure": pres_tbg
        }
}

app = FastAPI()


@app.get("/")
def home():
    return data


@app.get("/town/{town}")
def town(town: str):
    return data[town]


@app.put("/update_town/{town}")
def update_town(town: str, item: Item):
    data[town]["temperature"] = item.temperature
    data[town]["pressure"] = item.pressure
    return data[town]