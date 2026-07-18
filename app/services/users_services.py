from app.models.users import User
from sqlalchemy import select
from pydantic import EmailStr
from sqlalchemy.ext.asyncio.session import AsyncSession

class UserSchema:
    
    async def get_user(self, email: EmailStr, session: AsyncSession):
        statement = select(User).where(User.email == email)