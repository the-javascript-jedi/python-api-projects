from routers.schemas import UserBase
from sqlalchemy.orm.session import Session
from db.models import DbUser
from db.hashing import Hash

def create_user(db:Session,request:UserBase):
    new_user=DbUser(
        username=request.username,
        email=request.email,
        # password=request.password
        # hash the password
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user