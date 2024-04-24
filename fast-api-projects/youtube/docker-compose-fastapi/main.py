from fastapi import FastAPI
from datetime import date

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    print("item_id",item_id)
    print("q",q)
    return {"item_id": item_id, "q": q}

@app.get("/today")
async def read_today():
    return {"today": date.today().isoformat()}