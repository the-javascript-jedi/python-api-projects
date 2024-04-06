import shutil

from fastapi import APIRouter,Depends,File,UploadFile
from routers.schemas import PostBase, PostDisplay
from sqlalchemy.orm import Session
from database.database import get_db
from database import db_post
import string,random

router=APIRouter(
    prefix="/post",
    tags=["post"]
)

@router.post('')
def create(request:PostBase,db:Session=Depends(get_db)):
    return db_post.create(db,request)

@router.get("/all")
def posts(db:Session=Depends(get_db)):
    return db_post.get_all(db)

@router.delete("/{id}")
def delete(id:int,db:Session=Depends(get_db)):
    return db_post.delete(id,db)

@router.post('/image')
def upload_image(image:UploadFile=File(...)):
    # generate random string of letters to add to the name of our file
    letter=string.ascii_letters
    # generate a string of 6 letters and add to the string
    rand_str=''.join(random.choice(letter) for i in range(6))
    # Append to file name
    new = f'_{rand_str}.'
    filename=new.join(image.filename.rsplit('.',1))
    path=f'images/{filename}'
    # write file to images and close the buffer
    with open(path,"w+b") as buffer:
        shutil.copyfileobj(image.file,buffer)
        return {'filename':path}
