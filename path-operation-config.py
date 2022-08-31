from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Set, Union, List

app = FastAPI()


class Tags(Enum):
    items = "items"
    users = "users"


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()


@app.post("/items/", response_model=Item, tags=[Tags.items])
async def create_item(item: Item):
    """Create an item with all the information:
    
    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item


@app.get(
    "/items/", tags=[Tags.items], response_model=List[Item],
    summary="Read a list of items",
    description="Read a list of items with all the information, name, description, price, tax and a set of unique tags"
)
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/users/", tags=[Tags.users])
async def read_users():
    return [{"username": "johndoe"}]
