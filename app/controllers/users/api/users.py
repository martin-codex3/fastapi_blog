from fastapi import APIRouter
from app.services.users_services import UserServices
from sqlmodel.ext.asyncio.session import AsyncSession

users_router = APIRouter()

@users_router.get("/")
async def root():
    return {"message": "hey users"}