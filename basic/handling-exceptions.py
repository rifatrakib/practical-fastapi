from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler

app = FastAPI()
items = {"foo": "The Foo Wrestlers"}


class Item(BaseModel):
    title: str
    size: int


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."}
    )


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    print(f"An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


@app.post("/items/")
async def create_item(item: Item):
    return item


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404, detail="Item not found",
            headers={"X-Error": "There goes the error"}
        )
    return {"item": items[item_id]}


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


@app.get("/numbered-items/{item_id}")
async def read_numbered_item(item_id: int):
    if item_id < 1:
        raise HTTPException(status_code=418, detail="Not valid ID!")
    return {"item_id": item_id}
