from fastapi import FastAPI
from typing import Union, List
from dataclasses import field
from pydantic.dataclasses import dataclass

app = FastAPI()


@dataclass
class ItemBase:
    name: str
    description: Union[str, None] = None


@dataclass
class Author:
    name: str
    items: List[ItemBase] = field(default_factory=list)


@dataclass
class ItemExtended:
    name: str
    price: float
    tags: List[str] = field(default_factory=list)
    description: Union[str, None] = None
    tax: Union[float, None] = None


@app.post("/items/")
async def create_item(item: ItemExtended):
    return item


@app.get("/items/next/", response_model=ItemExtended)
async def read_next_item():
    return {
        "name": "Island In The Moon",
        "price": 12.99,
        "description": "A place to be be playin' and havin' fun",
        "tags": ["breater"],
    }


@app.post("/authors/{author_id}/items/", response_model=Author)
async def create_author_items(author_id: str, items: List[ItemBase]):
    return {"name": author_id, "items": items}


@app.get("/author/", response_model=List[Author])
async def get_authors():
    return [
        {
            "name": "Breaters",
            "items": [
                {
                    "name": "Island In The Moon",
                    "description": "A place to be be playin' and havin' fun",
                },
                {"name": "Holy Buddies"},
            ],
        },
        {
            "name": "System of an Up",
            "items": [
                {
                    "name": "Salt",
                    "description": "The kombucha mushroom people's favorite",
                },
                {"name": "Pad Thai"},
                {
                    "name": "Lonely Night",
                    "description": "The mostests lonliest nightiest of allest",
                },
            ],
        },
    ]
