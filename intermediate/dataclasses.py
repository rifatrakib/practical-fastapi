from typing import Union
from dataclasses import dataclass
from fastapi import FastAPI

app = FastAPI()


@dataclass
class Item:
    name: str
    price: float
    description: Union[str, None] = None
    tax: Union[float, None] = None


@app.post("/items/")
async def create_item(item: Item):
    return item
