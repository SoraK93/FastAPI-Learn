from typing import Annotated, Any
from fastapi import Depends, FastAPI

app = FastAPI()
fake_items_db = [{"item_name": "Foo"}, {
    "item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


common_dep = Annotated[CommonQueryParams, Depends()]


@app.get("/items/")
async def read_items(commons: common_dep):
    response = {}
    if commons.q:
        response["q"] = commons.q
    items = fake_items_db[commons.skip: commons.limit]
    response.update({"items": items})
    return response


@app.get("/users/")
async def read_users(commons: common_dep):
    return commons
