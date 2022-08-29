from typing import Union
from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get", ge=1, le=1000),
    q: Union[str, None] = Query(default=None, alias="item-query"),
    size: float = Query(gt=0, lt=10.5)
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if q:
        results.update({"size": size})
    return results
