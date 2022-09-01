from typing import Union, List
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(
    files: Union[List[bytes], None] = File(default=None, description="A file read as bytes")
):
    if not files:
        return {"message": "No file sent"}
    else:
        return {"file_sizes": [len(file) for file in files]}


@app.post("/upload-file")
async def create_upload_file(
    files: Union[List[UploadFile], None] = File(
        default=None,
        description="A file read as UploadFile"
    )
):
    if not files:
        return {"message": "No upload file sent"}
    else:
        return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
    <body>
    <form action="/files/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
    <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
    </body>
    """
    return HTMLResponse(content)
