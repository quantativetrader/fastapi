from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass

class Userout(BaseModel):
    
    email : EmailStr
    id : int
    created_at: datetime

    
    class Config:
       from_attributes = True

class return_request(PostBase):
    id: int
    created_at: datetime
    owener_id : int
    owner: Userout
    
    class Config:
       from_attributes = True
   
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    

   



    
class user_login(BaseModel):
    email: EmailStr
    password: str

    
class Token(BaseModel):
    access_token : str
    token_type: str


class TokenData(BaseModel):
    id: str
    
      