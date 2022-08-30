from typing import Union
from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
def read_items(user_agent: Union[str, None] = Header(default=None)):
    return {"User-Agent": user_agent}


@app.get("/strange-items/")
def read_strange_items(
    strange_header: Union[str, None] = Header(default=None, convert_underscores=False)
):
    return {"strange_header": strange_header}
