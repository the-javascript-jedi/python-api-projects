from fastapi import APIRouter,Depends,status,UploadFile,File
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from typing_extensions import List

from routers.schemas import PostBase, PostDisplay
from db.database import get_db
from db import db_post

import random
import string
import shutil

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

@router.get('/all',response_model=List[PostDisplay])
def posts(db:Session=Depends(get_db)):
    return db_post.get_all(db)

# upload an image
@router.post('/image')
def upload_image(image:UploadFile=File(...)):
    letters=string.ascii_letters
    rand_str=''.join(random.choice(letters) for i in range(6))
    new=f'_{rand_str}.'
    filename=new.join(image.filename.rsplit('.',1))
    path=f'images/{filename}'

    with open(path,"w+b") as buffer:
        shutil.copyfileobj(image.file,buffer)

    return {'filename':path}
