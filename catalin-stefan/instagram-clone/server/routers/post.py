from fastapi import APIRouter,Depends,status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from routers.schemas import PostBase, PostDisplay
from db.database import get_db
from db import db_post

router=APIRouter(
    prefix="/post",
    tags=['post']
)

image_url_types=['absolute','relative']

@router.post('',response_model=PostDisplay)
def create(request:PostBase,db:Session=Depends(get_db)):
    if not request.image_url_type in image_url_types:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="Parameter image_url_type can only take values 'absolute' or 'relative'")
        # raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY),detail="Parameter image_url_type")
    return db_post.create(db,request)