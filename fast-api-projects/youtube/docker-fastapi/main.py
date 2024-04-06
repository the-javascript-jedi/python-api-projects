from fastapi import FastAPI
# get environment variables
from os import environ as env

app = FastAPI()

@app.get("/")
def index():
    return {"details": f"Hello World! secret={env['MY_VARIABLE']}"}