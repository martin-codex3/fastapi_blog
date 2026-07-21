from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.post_schemas import PostResponse, CreatePost
from typing import Annotated
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.core.database import app_session
from app.services.post_services import PostServices
from sqlalchemy import select
from app.models.posts import Post

posts_router = APIRouter()
post_services = PostServices()

@posts_router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post(post_data: CreatePost, session: Annotated[AsyncSession, Depends(app_session)]):
    user_exists = await post_services.check_if_user_exists(
        post_data=post_data,
        session=session
    )
    
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found"
        )
    
    new_post = await post_services.create_new_post(
        post_data=post_data,
        session=session
    )
    
    return new_post


# getting a single post here 
@posts_router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
async def get_post(post_id: int, session: Annotated[AsyncSession, Depends(app_session)]):
    statement = await session.execute(
        select(Post).where(Post.id == post_id)
    )
    
    posts = statement.scalars().first()
    
    if posts:
        return posts
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Posts not found"
    )