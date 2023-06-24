from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from schemas import ProductBase

router=APIRouter(
    prefix="/templates",
    tags=['templates']
)

templates=Jinja2Templates(directory="templates")
# get template
@router.get("/products/{id}",response_class=HTMLResponse)
def get_product(id:str,request:Request):
    return templates.TemplateResponse(
        "product.html",
        {
            "request":request,
            "id":id
        }
    )