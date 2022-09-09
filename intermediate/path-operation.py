from fastapi import FastAPI, Request
from fastapi.routing import APIRoute
from typing import Set, Union
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()


def custom_data_reader(raw_body: bytes):
    return {
        "size": len(raw_body),
        "content": {
            "name": "custom",
            "price": 42,
            "description": "a custom description",
        }
    }


@app.post("/items/", )
@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "required": ["name", "price"],
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "price": {"type": "number"},
                            "description": {"type": "string"},
                        },
                    }
                }
            },
            "required": True,
        },
    },
)
async def create_item(item: Item, request: Request):
    """Create an item with all the information:
    
    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    \f
    :param item: user input
    """
    raw_body = await request.body()
    data = custom_data_reader(raw_body)
    return data


@app.get(
    "/items/", operation_id="unique_items_operation_id",
    openapi_extra={"x-aperture-labs-portal": "blue"},
)
async def read_items():
    return [{"item_id": "Foo"}]


@app.get("/all-items/", include_in_schema=False)
async def read_all_items():
    return [{"item_id": "Foo"}]


def route_names_as_operation_id(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function names.
    Should be called only after all routes have been added.
    If you do this, you have to make sure each one of your path operation functions has a unique name.
    Even if they are in different modules (Python files).
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


route_names_as_operation_id(app)
