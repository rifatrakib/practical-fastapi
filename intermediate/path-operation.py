from fastapi import FastAPI
from fastapi.routing import APIRoute

app = FastAPI()


@app.get("/items/", operation_id="unique_items_operation_id")
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
