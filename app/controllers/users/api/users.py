from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.schemas.user_schemas import UserResponseSchema
from app.schemas.user_schemas import CreateUserSchema
from typing import Annotated
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.core.database import app_session
from app.services.users_services import UserServices
from pydantic import EmailStr


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
    
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Account created successfully",
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
                "profile_image": new_user.profile_image,
                "image_path": new_user.image_path,
                "posted_at": new_user.posted_at
            }
        }
    )