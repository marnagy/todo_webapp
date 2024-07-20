from pydantic import BaseModel

# class TodoItemBase(BaseModel):
#     description: str = ""

# class TodoItemBaseCreate(Item):
#     pass

# class TodoItem(TodoItemBase):
#     id: int
#     todo_id: int
#     done: bool = False

#     # https://fastapi.tiangolo.com/tutorial/sql-databases/#use-pydantics-orm_mode
#     class Config:
#         from_attributes = True


# class TodoBase(BaseModel):
#     title: str
#     owner_id: int

# class TodoCreate(TodoBase):
#     pass

# class Todo(TodoBase)
#     id: int
#     items: list[TodoItem] = []

#     class Config:
#         from_attributes = True


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    hashed_password: str

    # todos: list[Todo] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
