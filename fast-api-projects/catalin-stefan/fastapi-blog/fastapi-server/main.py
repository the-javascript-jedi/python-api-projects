# uvicorn main:app --port 8080  --reload
from fastapi import FastAPI
from database import models
from database.database import engine
from routers import post
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()
app.include_router(post.router)

# create db
models.Base.metadata.create_all(engine)

# move files to a static path
#  name="images" is a parameter of mount function call
app.mount('/images',StaticFiles(directory="images"),name="images")

origins=[
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)