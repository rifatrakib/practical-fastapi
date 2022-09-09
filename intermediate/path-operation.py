from fastapi import FastAPI

app = FastAPI()


@app.get("/items/", operation_id="unique_items_operation_id")
async def read_items():
    return [{"item_id": "Foo"}]
