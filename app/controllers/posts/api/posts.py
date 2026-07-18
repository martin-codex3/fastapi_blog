from fastapi import APIRouter


posts_router = APIRouter()

@posts_router.get("/")
async def root():
    return {"message": "hey mate from posts"}