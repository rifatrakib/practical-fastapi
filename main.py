from enum import Enum
from uuid import UUID
from typing_extensions import Required
from typing import Union, List, Set, Dict
from datetime import datetime, time, timedelta
from pydantic import BaseModel, Field, Required, HttpUrl, EmailStr
from fastapi import FastAPI, Query, Path, Body, Cookie, Header

app = FastAPI()
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class ImageModel(BaseModel):
    url: HttpUrl
    name: str
    size: int


class Item(BaseModel):
    name: str = Field(example="foo")
    description: Union[str, None] = Field(
        default=None, title="description for the item", max_length=300,
        example="description to the item",
    )
    price: float = Field(gt=0, description="price must be greater than 0", example=30)
    tax: Union[float, None] = Field(example=2.4)
    tags: Set[str] = set()
    image: Union[List[ImageModel], None] = None


class Offer(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    items: List[Item]


class UserModel(BaseModel):
    username: str
    full_name: Union[str, None] = None


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


@app.get("/")
async def root():
    return {"message": "Application initialized"}


@app.get("/items/{item_id}/")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item


@app.get("/users/me/")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}/")
async def read_user(user_id: int):
    return {"user_id": user_id}


@app.get("/model/{model_name}/")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    
    if model_name.value == "resnet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    
    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}/")
async def read_file(file_path: str):
    return {"file_path": file_path}


@app.get("/users/{user_id}/items/{item_id}/")
async def read_user_item(user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    
    return item


@app.get("/item/{item_id}/")
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


@app.put("/items/{item_id}/")
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


@app.put("/single-item/{item_id}/")
async def update_single_item(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results


@app.post("/images/multiple/", response_model=List[ImageModel])
async def create_multiple_images(images: List[ImageModel] = Body(
        examples = {
                "normal": {
                    "summary": "a normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "url": "/images/1.png",
                        "name": "user_1",
                        "size": 35,
                    }
                },
                "converted": {
                    "summary": "example with converted data",
                    "description": "FastAPI can convert size `strings` to actual `numbers` automatically",
                    "value": {
                        "url": "/images/1.png",
                        "name": "user_1",
                        "size": "35",
                    }
                },
                "invalid": {
                    "summary": "invalid data example",
                    "description": "Invalid data is rejected with an error",
                    "value": {
                        "url": "-0945ui609",
                        "name": "tk34",
                        "size": "thirty five",
                    }
                }
            }
        )):
    return images


@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights


@app.get("read-item/{item_id}/")
def read_single_item(
            item_id: UUID,
            start_datetime: Union[datetime, None] = Body(default=None),
            end_datetime: Union[datetime, None] = Body(default=None),
            repeat_at: Union[time, None] = Body(default=None),
            process_after: Union[timedelta, None] = Body(default=None),
        ):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }


@app.get("/cookie-item/")
async def read_cookie_item(ads_id: Union[str, None] = Cookie(default=None)):
    return {"ads_id": ads_id}


@app.get("/header-item/")
async def read_header_item(user_agent: Union[str, None] = Header(default=None)):
    return {"User-Agent": user_agent}


@app.get("/strange-header/")
async def read_strange_header(
            strange_header: Union[str, None] = Header(default=None, convert_underscores=False),
        ):
    return {"strange_header": strange_header}


@app.get("/duplicate-headers/")
async def read_duplicate_headers(x_token: Union[List[str], None] = Header(default=None)):
    return {"X-Token values": x_token}


@app.post("/create-user/", response_model=UserOut, response_model_exclude_unset=True)
async def create_user(user: UserIn):
    return user
