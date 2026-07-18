from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
import uuid
from app.models.users import User
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.users import User

class Post(SQLModel, table = True):
    
    __tablename__ = "posts"
    
    id: int = Field(nullable=False, primary_key=True, index=True)
    title: str = Field(nullable=False, index=True)
    content: str = Field(nullable=False, index=True)
    date_posted: datetime = Field(default_factory=datetime.utcnow)
    user_id: uuid.UUID | None = Field(default=None, foreign_key="users.id")
    author: "User" | None = Relationship(back_populates="posts")
    