from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app.services.users_services import UserServices
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.user_schemas import CreateUserSchema
from app.core.database import app_session
from pydantic import EmailStr

users_router = APIRouter()
user_services = UserServices()

@users_router.get("/")
async def create_user_account(user_data: CreateUserSchema, session: AsyncSession = Depends(app_session)):
    email: EmailStr = user_data.email
    
    # we have to check if the user already exists here 
    user_exists = await user_services.check_user_exists(
        email = email,
        session = session
    )
    
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with tha email already exists"
        )
    else:
        new_user = await user_services.create_user_account(
            user_data = user_data,
            session = session
        )
        
        # we will return the json response here 
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "user": {
                    "id": new_user.id,
                    "username": new_user.username,
                    "email": new_user.email,
                    "is_profile_complete": new_user.is_profile_complete,
                    "profile_image": new_user.profile_image,
                    "image_path": new_user.image_path,
                    "created_date": new_user.image_path
                }
            }
        )