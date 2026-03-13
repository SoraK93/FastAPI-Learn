from typing import Annotated, Any
from fastapi import Cookie, Depends, FastAPI

app = FastAPI()


class QueryExtractor:
    def __init__(self, q: str | None = None):
        self.q = q


def query_or_cookie_extractor(
    q: Annotated[QueryExtractor, Depends()],
    last_query: Annotated[str | None, Cookie()] = None
):
    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_query(query_or_default: Annotated[str, Depends(query_or_cookie_extractor)]):
    return {"q_or_cookie": query_or_default}
