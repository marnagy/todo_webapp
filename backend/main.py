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

@app.get("/")
async def root():
    return {"message": "Hello World"}

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


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user

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
    data_dict = {"sub": db_user.username}
    print(f"Creating token on {data_dict}")
    access_token = crud.create_access_token(
        data=data_dict
    )
    return schemas.Token(access_token=access_token, token_type="bearer")

### authenticated endpoints ###

# authentication test
@app.get('/home') #, dependencies=[Depends(JWTBearer())])
def home(token: JWTBearer = Depends(JWTBearer())):
    return {'Welcome to': 'home page'}

@app.get('/todo') #, dependencies=[Depends(JWTBearer())])
def get_all_todos(db: Session = Depends(get_db), token = Depends(JWTBearer())):
    # user = crud.get_current_user(db, token)
    todos = crud.get_todos(db, token)
    return todos
    # return {
    #     {
    #         "id": todo.id,
    #         "title": todo.title,
    #         "items": [
    #             # for item in todo.items
    #         ]
    #     }
    #     for todo in todos
    # }

@app.post('/todo/add')
def add_todo(todo_create: schemas.TodoCreate, db: Session = Depends(get_db), token = Depends(JWTBearer())):
    todo = crud.add_todo(db, token, todo_create)
    return todo

@app.delete('/todo/{todo_id}')
def remove_item(todo_id: int, db: Session = Depends(get_db), token = Depends(JWTBearer())):
    try:
        res = crud.remove_todo(db, token, todo_id)
        return { 'success': res }
    except Exception as e:
        print(e)
        return { 'success': False }

@app.post('/todo/{todo_id}/item/add')
def add_todo(todo_id: int, todo_item_create: schemas.TodoItemCreate, db: Session = Depends(get_db), token = Depends(JWTBearer())):
    todo_item = crud.add_todo_item(db, token, todo_id, todo_item_create)
    return todo_item

@app.get('/todo/{todo_id}/item/{todo_item_id}/change_state')
def change_item_state(todo_id: int, todo_item_id: int, db: Session = Depends(get_db), token = Depends(JWTBearer())):
    todo_item = crud.change_state(db, token, todo_id, todo_item_id)
    return todo_item

@app.delete('/todo/{todo_id}/item/{todo_item_id}')
def remove_item(todo_id: int, todo_item_id: int, db: Session = Depends(get_db), token = Depends(JWTBearer())):
    try:
        res = crud.remove_item(db, token, todo_id, todo_item_id)
        return { 'success': res }
    except Exception as e:
        print(e)
        return { 'success': False }

# @app.post("/users/{user_id}/todos/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)

