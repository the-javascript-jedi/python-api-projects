# uvicorn main:app --port 8080  --reload
from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def hw():
    return "Hello World"