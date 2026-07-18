from sqlmodel import SQLModel, Field, Relationship
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.post import Post  

class User(SQLModel, table=True):
    
    __tablename__ = "users"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    username: str = Field(default=None, index=True, nullable=False, unique=True)
    email: str = Field(nullable=False, index=True)
    password: str = Field(nullable=False)
    is_profile_complete: bool = Field(default=False)
    profile_image: str | None = Field(
        nullable=True,
        default=None
    )
    created_date: datetime = Field(default_factory=datetime.utcnow)
    
    # for the relationship here 
    posts: list["Post"] = Relationship(back_populates="author")
    
    
    @property
    def image_path(self) -> str:
        if self.profile_image:
            return f"/media/profile_pictures/{self.profile_image}"
        else:
            return "default-image"