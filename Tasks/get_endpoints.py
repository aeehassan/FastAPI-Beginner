from fastapi import FastAPI

app = FastAPI(title="Practice on Get endpoints")


# Base
@app.get("/")
def root():
    return {"message": "API is running"}


@app.get("/health")
def get_status():
    return {"status": "ok"}


@app.get("/about")
def get_about():
    return {"name": "FastAPI Practice", "version": "1.0"}


@app.get("/greet")
def greeting():
    return {"greeting": "Hello, world"}


@app.get("/time")
def get_time():
    return {"timezone": "UTC", "format": "HH:MM"}


@app.get("/users/count")
def get_count():
    return {"count": 4}


@app.get("/skills")
def get_skills():
    return {"skills": ["Python", "FastAPI", "APIs"]}


@app.get("/config")
def get_config():
    return {"debug": True, "env": "development"}


@app.get("/features")
def get_features():
    return {"login": True, "payments": False}


@app.get("/summary")
def get_summary():
    return {"username": "abubakar", "active": True}
