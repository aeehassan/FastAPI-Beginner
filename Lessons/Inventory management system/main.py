# Inventory mgt system api for slaves

from fastapi import FastAPI, Path

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
        le=2,
    ),
):
    return inventory[id]
