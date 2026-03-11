from typing import Annotated, Any
from fastapi import Header, FastAPI
from pydantic import BaseModel

app = FastAPI()


class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []


@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None,
                     strange_header: Annotated[str | None, Header(
                         convert_underscores=False)] = None,
                     x_token: Annotated[list[str] | None, Header()] = None) -> dict[str, Any]:
    return {"User-Agent": user_agent, "strange_header": strange_header, "X-Token Value": x_token}


@app.get("/items-h/")
async def read_header(headers: Annotated[CommonHeaders, Header(convert_underscores=False)]):
    return headers
