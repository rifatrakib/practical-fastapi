from datetime import datetime
from typing import Union
from fastapi import FastAPI, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, ORJSONResponse, HTMLResponse, PlainTextResponse
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Union[str, None] = None


def generate_html_response():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    return JSONResponse(content=json_compatible_item_data)


@app.get("/legacy/")
def get_legacy_data():
    data = """
    <?xml version="1.0"?>
    <shampoo>
    <Header>
        Apply shampoo here.
    </Header>
    <Body>
        You'll have to use soap here.
    </Body>
    </shampoo>
    """
    return Response(content=data, media_type="application/xml")


@app.get("/items/", response_class=ORJSONResponse)
async def read_items():
    return ORJSONResponse([{"item_id": "Foo"}])


@app.get("/html-items/", response_class=HTMLResponse)
async def read_html_items():
    return generate_html_response()


@app.get("/text/", response_class=PlainTextResponse)
async def text_response():
    return "hello fasty"
