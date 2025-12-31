# --------------------------------------------
# Part 1
# --------------------------------------------

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(title="Request body tasks")


class Echo(BaseModel):
    message: str


class User(BaseModel):
    name: str
    age: int


class Profile(BaseModel):
    name: str
    skills: List[str]


class UserProfile(BaseModel):
    username: str
    password: str = Field(title="Password", min_length=4, max_length=8)


class Settings(BaseModel):
    darkmode: bool = False


@app.get("/")
def root():
    return "Hello world!!"


@app.post("/echo")
def echo_msg(echo: Echo):
    return {"message": echo.message}


@app.post("/users")
def display_user(user: User):
    return {
        "name": user.name,
        "age": user.age,
    }


@app.post("/profile")
def display_profile(profile: Profile):
    return {
        "name": profile.name,
        "skills": profile.skills,
    }


@app.post("/login")
def login(user: UserProfile):
    return {"username": user.username}


@app.post("/settings")
def tweak_settings(settings: Settings):
    return {"dark mode": settings.darkmode}


# --------------------------------------------
# Part 2
# --------------------------------------------
