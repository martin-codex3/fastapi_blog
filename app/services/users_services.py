from app.models.users import User
from sqlalchemy import select
from pydantic import EmailStr
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.schemas.user_schemas import CreateUserSchema

class UserServices:
    
    # we will get the user by the email or username
    async def get_user(self, email: EmailStr, session: AsyncSession):
        
        statement = await session.execute(
            select(User).where(User.email == email)
        )
        
        existing_user = statement.scalars().first()

        return existing_user
    
    # we will check if the user exists here 
    async def check_if_user_exists(self, email: EmailStr, session: AsyncSession):
        user_exists = await self.get_user(email = email, session = session)
        
        if user_exists:
            return True
        else:
            return False
    
    # we will create the user account here 
    async def create_user_account(self, user_data: CreateUserSchema, session: AsyncSession):
        user_dict = user_data.model_dump()
        
        new_user = User(**user_dict)
        
        session.add(new_user)
        
        await session.commit()
        
        await session.refresh(new_user)
        
        return new_user
        
        
        
        