from typing import Annotated, Any, Literal

from fastapi import FastAPI, Path, Body
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, description="The description of the item", max_length=300
    )
    price: float = Field(
        gt=0, description="The price must be greater than zero")
    tax: float | None = None
    tags: set[str] = set()
    image: list[Image] | None = None


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]


class Path_Params(BaseModel):
    item_id: int = Field(title="The ID of the item to get", ge=0, le=1000)


class Body_Params(BaseModel):
    q: str | None = Field(default=None, examples=[None])
    item: Item | None = Field(default=None)


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer


@app.put("/items/item-{item_id}")
async def update_item_only(item_id: int, b_params: Annotated[Body_Params, Body()]):
    results: dict[str, Any] = {"item_id": item_id}
    if b_params.q:
        results["q"] = b_params.q
    if b_params.item:
        results["item"] = b_params.item
    return results


@app.put("/items/image/{item_id}")
@app.put("/items/{item_id}")
async def update_item(
        p_params: Annotated[Path_Params, Path()],
        b_params: Annotated[Body_Params, Body()],
        quality: Literal["good", "bad"]):
    results: dict[str, Any] = {"item_id": p_params.item_id}
    if b_params.q:
        results["q"] = b_params.q
    if b_params.item:
        results["item"] = b_params.item
        if b_params.item.price > 10:
            results["quality"] = quality
        else:
            results["quality"] = quality
    return results
