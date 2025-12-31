# Inventory mgt system api for slaves

from fastapi import FastAPI, Path, Query, HTTPException, status

# When making a query optional, it is suggested
# to use the typing class
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

inventory = {
    1: {
        "name": "Audu",
        "price": 900,
    },
    2: {
        "name": "Lucas",
        "price": 1500,
    },
}


@app.get("/")
def root():
    return "Hello world!"


# Endpoint/path parameters - Basic
@app.get("/items-basic/{item_id}")
def get_item_basic(item_id: int):
    try:
        return inventory[item_id]
    except Exception:
        return f"{item_id} is not yet in stock :("


# Endpoint/path parameters - Advanced
@app.get("/items-advanced/{id}")
def get_item_advanced(
    id: int = Path(
        description="Returns info about a specific item",
        ge=1,
    ),
):
    return inventory[id]


## Query paramters - variables that come after '?' Eg. ?name=Audu&age=12
# An endpoint taking one query parameter
@app.get("/get-by-name")
def get_user(name: Optional[str] = None):
    for id in inventory:
        if inventory[id]["name"] == name:
            return inventory[id]

    return "User not found"


# Request body
# To send data without showing in our url.
# To send info to a db commonly
#
# Steps
# - Create a pydantic class
# - Accept that class as the fn's input
#
# Though, in fast, you can give default values
# within the pydantic model
#

# If uvicorn glitches, press enter twice
#


class Item(BaseModel):
    name: str
    price: int


class UpdateItem(BaseModel):
    name: str = None
    price: int = None


@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        return "It already exists"

    # This works bcoz fast serializes the item obj to json
    inventory[item_id] = item
    return inventory[item_id]


# put method - uses request body as well but
# with more optionals
@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        return "It doesn't exist"

    if item.name != None:  # noqa: E711
        inventory[item_id].name = item.name
    if item.price != None:  # noqa: E711
        inventory[item_id].price = item.price

    return inventory[item_id]


@app.delete("/delete-item")
def del_item(
    item_id: int = Query(..., description="Only delete items within inventory"),
):
    if item_id not in inventory:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Ïtem does not exist"
        )

    del inventory[item_id]
    return "Success"


# Status codes and error response
# - Import HTTPException and status - for the right status code of a specific endpoint
# - Raise exception with details and status_code as paramters
#
print(status)
