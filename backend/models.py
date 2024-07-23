from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    todos = relationship("Todo", back_populates="owner")

    def __str__(self) -> str:
        return str({
            'id': self.id,
            'username': self.username,
            'hashed_password': self.hashed_password
        })


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="todos")
    items = relationship("TodoItem", back_populates="todo")

class TodoItem(Base):
    __tablename__ = "todo_items"

    id = Column(Integer, primary_key=True)
    todo_id = Column(Integer, ForeignKey("todos.id"))
    done = Column(Boolean, nullable=False)
    description = Column(String, nullable=False)

    todo = relationship("Todo", back_populates="items")
