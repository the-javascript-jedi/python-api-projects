from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from starlette.background import BackgroundTasks

from schemas import ProductBase
from custom_log import log

router=APIRouter(
    prefix="/templates",
    tags=['templates']
)

templates=Jinja2Templates(directory="templates")
# get template
@router.get("/products/{id}",response_class=HTMLResponse)
def get_product(id:str,request:Request,bt:BackgroundTasks):
    bt.add_task(log_template_call,f"Template read for product with id {id}")
    return templates.TemplateResponse(
        "product.html",
        {
            "request":request,
            "id":id
        }
    )

def log_template_call(message:str):
    log("MyApi",message)