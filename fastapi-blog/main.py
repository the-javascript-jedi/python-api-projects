# uvicorn main:app --port 8080  --reload
from fastapi import FastAPI
from database import models
from database.database import engine
from routers import post

app=FastAPI()
app.include_router(post.router)

# create db
models.Base.metadata.create_all(engine)