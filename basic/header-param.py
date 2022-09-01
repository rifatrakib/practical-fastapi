from typing import Union, List
from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(user_agent: Union[str, None] = Header(default=None)):
    return {"User-Agent": user_agent}


@app.get("/strange-items/")
async def read_strange_items(
    strange_header: Union[str, None] = Header(default=None, convert_underscores=False)
):
    return {"strange_header": strange_header}


@app.get("/duplicate-header-items")
async def duplicate_header_items(
    x_token: Union[List[str], None] = Header(default=None)
):
    return {"X-Token values": x_token}
