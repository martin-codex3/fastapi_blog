from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String, DateTime
from typing import List
from app.utils.base import Base
import uuid
from datetime import UTC, datetime
from app.models.posts import Post


class User(Base):
    
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(default_factory=uuid.uuid4, primary_key=True, default=None)
    username: Mapped[str] = mapped_column(String(30), default=None, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(default=None, index=True, nullable=False, unique=True)
    profile_image: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    posted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(UTC))

    posts: Mapped[List[Post]] = relationship(back_populates="users")
    
    @property
    def image_path(self) -> str:
        if self.profile_image:
            return f"/media/profile_pics/{self.profile_image}"
        else:
            return "/static/default.jpg"