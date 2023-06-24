from fastapi.requests import Request
from fastapi.param_functions import Depends
from fastapi import APIRouter

router=APIRouter(
    prefix="/dependencies",
    tags=["dependencies"]
)
#//dependency function
def convert_headers(request:Request,separator:str="^^"):
    out_headers=[]
    for key,value in request.headers.items():
        out_headers.append(f"{key} __{separator}__ {value}")
    return out_headers

@router.get("")
def get_items(separator:str='--',headers=Depends(convert_headers)):
    return{
        'items':['a','b','c'],
        'headers':headers
    }

@router.post("/new")
def create_item(headers=Depends(convert_headers)):
    return{
        'result':'new item created',
        'headers':headers
    }