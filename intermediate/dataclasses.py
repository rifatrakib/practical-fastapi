from fastapi import FastAPI
from typing import Union, List
from dataclasses import dataclass, field

app = FastAPI()


@dataclass
class Item:
    name: str
    price: float
    tags: List[str] = field(default_factory=list)
    description: Union[str, None] = None
    tax: Union[float, None] = None


@app.post("/items/")
async def create_item(item: Item):
    return item


@app.get("/items/next/", response_model=Item)
async def read_next_item():
    return {
        "name": "Island In The Moon",
        "price": 12.99,
        "description": "A place to be be playin' and havin' fun",
        "tags": ["breater"],
    }
