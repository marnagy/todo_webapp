from sqlalchemy.orm import Session

import models
import schemas

import random

ALPHANUMS = "0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM,<.>/?;:'\"\\[]\{\}=-_+!@#$%^&*()"
def get_new_salt() -> str:
    return random.choices(ALPHANUMS, k=20)


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.User).offset(offset).limit(limit).all()

def create_user(db: Session, user_create: schemas.UserCreate):
    salt = get_new_salt()
    password_hashed = hash(user_create.password + salt)
    db_user = models.User(
        username=user_create.username,
        hashed_password=password_hashed,
        salt=salt,
    )
    db.add(db_user)
    db.commit()
    db_user = get_user_by_username(db, username=user_create.username)
    return db_user


