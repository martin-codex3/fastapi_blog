from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Text, ForeignKey, Integer, String, DateTime
from app.utils.base import Base
from datetime import datetime, UTC
import uuid
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.users import User

class Post(Base):
    
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(Integer, default=None, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    posted_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(UTC))
    
    # for the foreign key here 
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    user: Mapped[Optional[User]] = relationship(back_populates="posts")
    