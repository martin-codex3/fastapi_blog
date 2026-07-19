from fastapi import APIRouter, HTTPException, status
from app.schemas.post_schemas import PostResponse
posts_router = APIRouter()

@posts_router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def root():
    return {"message": "hey mate from posts"}