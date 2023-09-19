from fastapi import Depends,responses,APIRouter,status,HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from ..database import get_db
from .. import schemas,utils,models
from . import users,oauth2


router = APIRouter(tags = ["authentication"])
@router.post("/login")

def login(user_credentials:OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user= db.query(models.Users).filter(models.Users.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"invalid credintials")
    

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,detail= f"invalid credentials")
    
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    
    return{"access_token": access_token, "token_type": "bearer"}






     