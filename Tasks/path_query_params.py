from fastapi import FastAPI, Path, Query
from typing import List

# These Classes
# Path is more for data description
# Enum is more for specifying values that a parameter
# can only accept like it should only accept 0,1,2,3
app = FastAPI(title="Path & Query parameters")


@app.get("/")
def root():
    return "Hello world!!"


@app.get("/users/{user_id}")
def get_user(user_id: int = Path(ge=0)):
    return {"user_id": user_id}


@app.get("/books/{title}")
def get_book(title: str):
    return {"title": "fastapi"}


@app.get("/search")
def get_response(q: str):
    return {"query": q}


@app.get("/items")
def get_item(page: int = 1):
    return {"page": page}


@app.get("/products/{product_id}")
def get_product(product_id: int, category: str):
    return {"product_id": product_id, "category": category}


@app.get("/users/{user_id}/posts/{post_id}")
def get_user_and_post(user_id: int, post_id: int):
    return {
        "user_id": user_id,
        "post_id": post_id,
    }


@app.get("/filter")
def get_filter(status: str, sort: str):
    return {"status": status, "sort": sort}


@app.get("/orders/{order_id}")
def get_order(order_id: int, details: bool = False):
    return {"order_id": order_id, "details": details}


@app.get("/tags")
def get_tags(tags: List[str] = Query([])):
    return {"tags": tags}


@app.get("/summary/{username}")
def get_user_summary(username: str, active: bool = True):
    return {"username": username, "active": active}
