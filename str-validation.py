from typing import List, Union
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
    ),
    hidden_query: Union[str, None] = Query(default=None, include_in_schema=False)
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    if hidden_query:
        results.update({"hidden_query": hidden_query})
    return results
