from enum import Enum
from typing import Union, List
from typing_extensions import Required
from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, Required

app = FastAPI()
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


class UserModel(BaseModel):
    username: str
    full_name: Union[str, None] = None


@app.get("/")
async def root():
    return {"message": "Application initialized"}


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}


@app.get("/model/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    
    if model_name.value == "resnet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    
    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    
    return item


@app.get("/item/{item_id}")
async def read_items(
        item_id: int = Path(title="id of the item to get", gt=1, le=1000),
        q: Union[List[str], None] = Query(
            default=["foo", "bar"], min_length=2, max_length=50,
            alias="item-list", deprecated=True, regex="\w+", title="query list",
            description="provide a list of strings which only contains letters"),
        size: float = Path(ge=0, lt=1),
        visible_query: Union[str, None] = Query(default=Required),
        hidden_query: Union[str, None] = Query(default=None, include_in_schema=False)):
    
    results = {"item_id": item_id, "size": size}
    if q:
        results.update({"q": q})
    return results


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
async def update_item(
        *, item_id: int = Path(title="id of the item to query for", ge=0, lt=1000),
        q: Union[str, None] = None,
        user: UserModel(embed=True),
        importance: int = Body(),
        item: Union[Item, None] = None):
    result = {"item_id": item_id, "user": user, "importance": importance}
    if q:
        result.update({"q": q})
    if item:
        result.update({"item": item})
    return result
