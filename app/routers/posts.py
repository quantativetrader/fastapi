from typing import Optional, List
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas
from .. database import get_db
from . import oauth2


router = APIRouter(prefix= "/posts", tags= ["posts"])
 
@router.get("/", response_model= List[schemas.return_request])  #getting post
async def get_posts(db: Session = Depends(get_db),limit: int = 10, skip: int = 0, 
                    search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post("/", status_code= status.HTTP_201_CREATED , response_model= schemas.return_request)   # creating new post 
async def create_post(post: schemas.CreatePost , db: Session = Depends(get_db)):
                      
   
#    print(current_user.id)
   new_post = models.Post(**post.dict())   #dictonary unpacking(**.dict())
   db.add(new_post)
   db.commit()
   db.refresh(new_post)
   
   return new_post



@router.get("/{id}", response_model= schemas.return_request)     #id is the path parameter
async def find_post(id: int, db: Session = Depends(get_db)):   #validation by fastapi that parameter passed should be int
   
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id:{id} not found")
    return{"post_details": post}

@router.delete("/{id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id :{id} does not exist")
    
    post.delete(synchronize_session = False)
    db.commit()

    return Response(status_code= status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model= schemas.return_request)
def update_post(id: int, updated_post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with id :{id} does not exist")
    
    post_query.update(updated_post.dict(),synchronize_session = False)
    db.commit()
    return post_query.first()
