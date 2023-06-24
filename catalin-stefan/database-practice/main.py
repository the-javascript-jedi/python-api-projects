# uvicorn main:app --port 8086  --reload
# http://127.0.0.1:8086/docs
from typing import Optional
from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse

from router import blog_get, blog_post, user, article, product,file,dependencies
from auth import authentication
from db.database import engine
from db import models
from exceptions import StoryException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from templates import templates
import time
from client import html
from fastapi.websockets import WebSocket

app = FastAPI()
app.include_router(dependencies.router)
app.include_router(templates.router)
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)

@app.get('/hello')
def index():
  return {'message': 'Hello world!'}

@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
  return JSONResponse(
    status_code=418,
    content={'detail': exc.name}
  )

# @app.exception_handler(HTTPException)
# def custom_handler(request: Request, exc: StoryException):
#   return PlainTextResponse(str(exc), status_code=400)
@app.get("/")
async def get():
  return HTMLResponse(html)
# web socket code
clients=[]

@app.websocket("/chat")
async def websocket_endpoint(websocket:WebSocket):
  await websocket.accept()
  clients.append(websocket)
  while True:
    data = await websocket.receive_text()
    for client in clients:
      await client.send_text(data)

models.Base.metadata.create_all(engine)

@app.middleware("http")
async def add_middleware(request:Request,call_next):
  start_time=time.time()
  response=await call_next(request)
  duration=time.time()-start_time
  # modify the duration and add it in headers
  response.headers['duration']=str(duration)
  return response


origins = [
  'http://localhost:3000'
]

app.add_middleware(
  CORSMiddleware,
  allow_origins = origins,
  allow_credentials = True,
  allow_methods = ["*"],
  allow_headers = ['*']
)

app.mount("/files",StaticFiles(directory="files"),name="files")