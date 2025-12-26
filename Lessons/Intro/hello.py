# Import FastAPI class
# /docs is used for testing your api
#
from fastapi import FastAPI

# Instantiate API object
app = FastAPI()

# Endpoint: A resource you're trying to access on
# a server. eg. /user, /product
#
# Base server eg. localhost
#

# Creating an endpoint


@app.get("/")
def get_message():
    return {
        "user": "aeehassan",
        "message": "Hello world!!",
    }


@app.get("/about")
def about():
    return "About me!!"
