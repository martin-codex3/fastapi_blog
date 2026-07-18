from fastapi import APIRouter

users_router = APIRouter()

@users_router.get("/")
async def get_users():
    return {"message": "users here"}