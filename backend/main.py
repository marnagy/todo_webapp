# pip
from fastapi import Depends, FastAPI, HTTPException, status, Header
from sqlalchemy.orm import Session

# custom modules
import crud
import models
import schemas
from bearer import JWTBearer
from database import SessionLocal, engine

# standard lib
import os
from typing import Annotated

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/add", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user is not None:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user_create=user)


# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post('/token', response_model=schemas.Token)
def get_token(user_create: schemas.UserCreate, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    db_user = crud.authenticate_user(db, user_create)
    if db_user is None:
        return credentials_exception
    # create JWT token
    access_token = crud.create_access_token(
        data={"sub": db_user.username}
    )
    return schemas.Token(access_token=access_token, token_type="bearer")

@app.get('/home', dependencies=[Depends(JWTBearer())])
def home():
    return {'Welcome to': 'home page'}


# @app.post("/users/{user_id}/todos/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)




@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.post("/todo/add")
# async def add_todo(todo):
    

# @app.get("/todo/{todo_id}")
# async def get_todo(todo_id: int):
#     pass
