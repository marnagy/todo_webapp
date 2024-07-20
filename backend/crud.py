from sqlalchemy.orm import Session
from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import models
import schemas

import random
from typing import Optional, Annotated
from datetime import datetime, timedelta, timezone
import os

SECRET_KEY = os.getenv('BACKEND_SECRET_KEY')
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = int(os.getenv('TOKEN_EXPIRE_MINUTES'))

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

def create_user(db: Session, user_create: schemas.UserCreate):
    password_hashed = get_password_hash(user_create.password)
    db_user = models.User(
        username=user_create.username,
        hashed_password=password_hashed,
    )
    db.add(db_user)
    db.commit()
    db_user = get_user_by_username(db, username=user_create.username)
    return db_user

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

def get_current_user(db: Session, token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(username=username)
    except InvalidTokenError:
        return None
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        return None
    return user
