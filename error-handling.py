from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler
)
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


class Item(BaseModel):
    title: str
    size: int


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. Error Occurred."}
    )


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    # return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request=request, exc=exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # message = "Validation error:"
    # for error in exc.errors():
    #     message += f"\nField: {error['loc']}, Error: {error['msg']}"
    # return PlainTextResponse(message, status_code=400)
    # return JSONResponse(
    #     status_code=422,
    #     content=jsonable_encoder({"detail": exc.errors(), "body": exc.body})
    # )
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request=request, exc=exc)


@app.post("/items/")
async def create_item(item: Item):
    return item


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(
            status_code=418, detail="Nope! You are not authorized.")
    return {"item_id": item_id}


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}
