from typing import List
from fastapi import FastAPI, Query
from pydantic import Required

app = FastAPI()


@app.get("/items/")
async def read_items(
    q: List[str] = Query(
        default=["foo", "bar"], min_length=3, max_length=50, regex="^fixedquery$",
        alias="item-query", title="Query string",
        description="Query string for the items to search in the database that have a good match",
        deprecated=True
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
