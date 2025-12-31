# Tasks 1 - 5 on endpoints

from fastapi import FastAPI, Path


app = FastAPI()

# Database
users = {
    1: {
        "name": "Faruq",
        "age": 18,
    },
    2: {
        "name": "Abubakar",
        "age": 20,
    },
    3: {
        "name": "Abdullahi",
        "age": 17,
    },
    4: {
        "name": "Faisal",
        "age": 16,
    },
}


# basic endpoint 🏁
@app.get("/")
def hello():
    return {"message": "Welcome to FastAPI"}


# endpoint with path parameter 🏁
@app.get("/users/{user_id}")
def get_user(
    user_id: int = Path(
        description="Retrieve info about a particular user", ge=1, le=4
    ),
):
    try:
        return users[user_id]
    except Exception as e:
        return str(e)


# endpoint w/query parameter 🏁
@app.get("/search")
def search(q: str):
    return {
        "query": q,
    }


# Multiple parameters in an endpoint 🏁
@app.get("/items/{item_id}")
def get_item(item_id: int, category: str):
    try:
        return {
            "item_id": item_id,
            "category": category,
        }
    except Exception as e:
        return str(e)


# Returning structured json
profile = {
    "name": "Abubakar",
    "skills": ["Python", "FastAPI"],
    "active": True,
}


@app.get("/profile")
def get_profile():
    return profile
