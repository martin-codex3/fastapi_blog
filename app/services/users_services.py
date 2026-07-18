from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.users import User
from sqlmodel import select
from app.schemas.user_schemas import CreateUserSchema
from pydantic import EmailStr
import uuid

class UserServices:
    
    async def get_user(self, email: EmailStr, session: AsyncSession):
        
        statement = select(User).where(User.email == email)
        
        results = await session.exec(statement)
        
        return results.first()
    
    # checking if the user exists here 
    async def check_user_exists(self, email: EmailStr, session: AsyncSession):
        
        user = await self.get_user(email = email, session = session)
        
        if user is not None:
            return False
        else:
            return True
    
    # we will create the user account here 
    async def create_user_account(self, user_data: CreateUserSchema, session: AsyncSession):
        new_user_dict = user_data.model_dump()
        
        new_user = User(**new_user_dict)
        
        session.add(new_user)
        
        await session.commit()
        
        await session.refresh(new_user)
        
        return new_user
    
    # getting a user by their id 
    async def get_user_by_id(self, user_id: uuid.UUID, session: AsyncSession):
        statement = select(User).where(User.id == user_id)
        
        user = await session.exec(statement)
        
        if user:
            return user
        else:
            return None
        
        