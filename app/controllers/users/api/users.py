from fastapi import APIRouter, status, HTTPException, Depends
from app.schemas.user_schemas import UserResponseSchema
from app.schemas.user_schemas import CreateUserSchema
from typing import Annotated
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.core.database import app_session
from app.services.users_services import UserServices
from pydantic import EmailStr
from sqlalchemy import select
from app.models.users import User
import uuid


users_router = APIRouter()
user_services = UserServices()

@users_router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema)
async def create_user_account(user_data: CreateUserSchema, session: Annotated[AsyncSession, Depends(app_session)]):
    email: EmailStr = user_data.email
    user_exists = await user_services.check_if_user_exists(
        email = email,
        session = session
    )
    
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with that email already exists"
        )
    
    # we will create the new user here 
    new_user = await user_services.create_user_account(
        user_data = user_data,
        session = session
    )
    
    return new_user


# getting a single user here 
@users_router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
async def get_user(user_id: uuid.UUID, session: Annotated[AsyncSession, Depends(app_session)]):
    statement = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = statement.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to get user with that id"
        )
    
    return user
        