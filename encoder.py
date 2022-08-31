from typing import Union
from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()
fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Union[str, None] = None


@app.put("/items/{id}")
async def update_item(id: str, item: Item):
    item_data = jsonable_encoder(item)
    fake_db[id] = item_data
    return item_data
