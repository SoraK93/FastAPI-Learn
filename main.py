from enum import Enum
from fastapi import FastAPI, Path, Query
from pydantic import AfterValidator, BaseModel
from typing import Any, Annotated
import random


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI(
    title="My First FastAPI - App",
    version="0.2.0",
    description="This is a project I am building to learn FastAPI"
)

fake_items_db = [{"item_name": "Foo"}, {
    "item_name": "Bar"}, {"item_name": "Baz"}]

data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}


def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError(
            "Invalid ID format, it must start with 'isbn-' or 'imdb-'")
    return id


@app.get("/items/{item_id}", tags=["items"])
async def read_items(
    item_id: Annotated[str, Path(title="The ID of the item to get"), AfterValidator(check_valid_id)],
    q: Annotated[str | None, Query(alias="item-query")] = None
) -> dict[str, Any]:
    results: dict[str, int | str | None] = {"item_id": item_id}
    if q:
        results["q"] = q
    if item_id:
        results["data"] = data.get(item_id)
    else:
        item_id, item = random.choice(list(data.items()))
        results["data"] = item
    return results


@app.get("/items-q/", tags=["items"])
async def read_items_query(
    q: Annotated[
        str | None,
        Query(
            title="Query String",
            alias="item-query",
            description="Query string for the items to search in the database that have a good match",
            max_length=50,
            pattern="^fixedquery$",
            deprecated=True)] = None
):
    results: dict[str, list[dict[str, str]] | str] = {
        "items": fake_items_db
    }
    if q:
        results["q"] = q
    return results


@app.post("/items/", tags=["items"])
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item


@app.put("/items-update/{item_id}", tags=["items"])
async def update_item(item_id: int, item: Item, q: str | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result


@app.get("/items-get/{item_id}", tags=["items"])
async def read_item(item_id: str, needy: str, skip: int = 0, limit: int | None = None):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item


@app.get("/users/{user_id}/items/{item_id}", tags=["users"])
async def read_user_item(user_id: int, item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@app.get("/models/{model_name}", tags=["models"])
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some rediduals"}


@app.get("/files/{file_path:path}", tags=["files"])
async def read_file(file_path: str):
    return {"file_path": file_path}
