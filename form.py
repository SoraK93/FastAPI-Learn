from typing import Annotated, Any
from pydantic import BaseModel
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()


class FormData(BaseModel):
    username: str
    password: str


@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data


@app.post("/files/")
async def create_file(file: Annotated[bytes, File(description="A file read as bytes")],
                      fileb: Annotated[UploadFile, File()],
                      token: Annotated[str, Form()]) -> dict[str, Any]:
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }


@app.post("/uploadfile/")
async def create_upload_file(files: Annotated[list[UploadFile], File(description="A file read as UploadFile")]):
    if not files:
        return {"message": "No upload file sent"}
    else:
        return {"filename": [file.filename for file in files]}


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
    return HTMLResponse(content=content)
