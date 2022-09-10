from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/headers-and-object/")
def get_headers(response: Response):
    response.headers["X-Cat-Dog"] = "alone in the world"
    return {"message": "headers set"}


@app.get("/headers/")
def get_required_headers():
    content = {"message": "hello"}
    headers = {"X-Cat-Dog": "alone in the world", "Content-Language": "en-US"}
    return JSONResponse(content=content, headers=headers)
