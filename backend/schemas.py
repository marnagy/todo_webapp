from pydantic import BaseModel

import models

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


class TodoBase(BaseModel):
    title: str
    owner_id: int

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    title: str
    owner_id: int
    # items: list[TodoItem] = []

    @staticmethod
    def from_db(db_todo: models.Todo) -> 'Todo':
        return Todo(
            id=db_todo.id,
            title=db_todo.title,
            owner_id=db_todo.owner_id,
            # items=[
            #     for item in db_todo.items
            # ]
        )

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    hashed_password: str

    todos: list[Todo] = []

    @staticmethod
    def from_db(db_user: models.User) -> 'User':
        return User(
            id=db_user.id,
            username=db_user.username,
            # ! HASH CANNOT LEAVE SERVER
            hashed_password='',
            todos=[
                Todo.from_db(todo)
                for todo in db_user.todos
            ]
        )

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
