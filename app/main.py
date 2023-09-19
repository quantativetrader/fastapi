from typing import Optional, List
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from pydantic import BaseModel
from random import randrange 
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . routers import posts,users,auth

from . import models
from .database import engine,get_db
from .config import settings



models.Base.metadata.create_all(bind=engine)
app = FastAPI()    #creating instance of the FastAPI


    
while True:        #connecting to database without sql alchemy

    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', 
                            password = 'darryl123', cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print("database connection is succesful")
        break
    except Exception as error:
        print("connection to database failed")
        print("error", error)
        time.sleep(5)
        
        
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)












