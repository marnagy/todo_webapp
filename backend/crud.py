from sqlalchemy.orm import Session
from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import models
import schemas

import random
from typing import Optional, Annotated, Iterable, TypeVar
from datetime import datetime, timedelta, timezone
import os

SECRET_KEY = os.getenv('BACKEND_SECRET_KEY')
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = int(os.getenv('TOKEN_EXPIRE_MINUTES'))

T = TypeVar('T')

def first(iter: Iterable[T]) -> T:
    should_continue = True
    for item in iter:
        return item

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

ALPHANUMS = "0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM,<.>/?;:'\"\\[]\{\}=-_+!@#$%^&*()"
def get_new_salt() -> str:
    return ''.join(random.choices(ALPHANUMS, k=20))

def create_hash(password: str, salt: str) -> int:
    return hash(password + salt)

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.User).offset(offset).limit(limit).all()

def get_todos(db: Session,
              token: Annotated[str, Depends(oauth2_scheme)]) -> list[schemas.Todo]:
    db_user = get_current_user(db, token)
    user = schemas.User.from_db(db_user)
    return user.todos

def add_todo(db: Session,
             token: Annotated[str, Depends(oauth2_scheme)],
             todo_create: schemas.TodoCreate) -> schemas.Todo:
    db_user = get_current_user(db, token)
    db_todo = models.Todo(
        title=todo_create.title
    )
    db_user.todos.append(db_todo)
    db.commit()
    return schemas.Todo.from_db(db_todo)

def add_todo_item(db: Session,
                  token: Annotated[str, Depends(oauth2_scheme)],
                  todo_id: int,
                  todo_item_create: schemas.TodoItemCreate) -> schemas.TodoItem:
    db_user = get_current_user(db, token)
    db_todos = list(filter(lambda todo: todo.id == todo_id, db_user.todos))
    if len(db_todos) != 1:
        return None
    db_todo = db_todos[0]
    db_todo_item = models.TodoItem(
        done=False,
        description=todo_item_create.description
    )
    db_todo.items.append(db_todo_item)
    db.commit()
    return schemas.TodoItem.from_db(db_todo_item)

def change_state(db: Session,
                 token: Annotated[str, Depends(oauth2_scheme)],
                 todo_id: int,
                 todo_item_id: int) -> schemas.TodoItem:
    db_user = get_current_user(db, token)
    db_todos = list(filter(lambda todo: todo.id == todo_id, db_user.todos))
    if len(db_todos) != 1:
        return None
    db_todo = db_todos[0]
    db_todo_items = list(filter(lambda todo: todo.id == todo_id, db_todo.items))
    if len(db_todo_items) != 1:
        return None
    db_todo_item = db_todo_items[0]
    db_todo_item.done = not db_todo_item.done
    db.commit()
    return schemas.TodoItem.from_db(db_todo_item)

def create_user(db: Session, user_create: schemas.UserCreate) -> schemas.User:
    password_hashed = get_password_hash(user_create.password)
    db_user = models.User(
        username=user_create.username,
        hashed_password=password_hashed,
    )
    db.add(db_user)
    db.commit()
    db_user = get_user_by_username(db, username=user_create.username)
    return schemas.User.from_db(db_user)

def authenticate_user(db: Session, user_create: schemas.UserCreate) -> Optional[schemas.User]:
    db_user = get_user_by_username(db, user_create.username)
    if not db_user:
        return None
    if not verify_password(user_create.password, db_user.hashed_password):
        return None
    return db_user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(db: Session, token: Annotated[str, Depends(oauth2_scheme)]) -> Optional[models.User]:
    # credentials_exception = HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Could not validate credentials",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        username: str = payload.get("sub")
        print(username)
        if username is None:
            return None
    except InvalidTokenError:
        return None
    db_user = get_user_by_username(db, username=username)
    return db_user
