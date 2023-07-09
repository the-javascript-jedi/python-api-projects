from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# model schema for python backend
class DbUser(Base):
    __tablename__="user"
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String)
    email = Column(String)
    password = Column(String)
    items=relationship('DbPost',back_populates='user')

class DbPost(Base):
    __tablename__="post"
    id = Column(Integer, primary_key=True, index=True)
    image_url=Column(String)
    image_url_type=Column(String)
    caption=Column(String)
    timestamp=Column(DateTime)
    user_id=Column(Integer,ForeignKey('user.id'))
    user=relationship('DbUser',back_populates='items')