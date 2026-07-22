from fastapi import APIRouter, HTTPException, status, Depends, Request
from app.schemas.post_schemas import PostResponse, CreatePost
from typing import Annotated
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.core.database import app_session
from app.services.post_services import PostServices
from sqlalchemy import select
from app.models.posts import Post
import uuid
from app.models.users import User
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


posts_router = APIRouter()
post_services = PostServices()

# we will configure the jinja template here 
templates = Jinja2Templates(directory="templates")

# for the jinja templates here 
@posts_router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home(request: Request, session: Annotated[AsyncSession, Depends(app_session)]):
    # we will fetch all the posts here 
    statement = await session.execute(
        select(Post)
    )
    
    posts = statement.scalars().all()
    
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        status_code=status.HTTP_200_OK,
        context={"posts": posts}
    )


# for getting a single post here 
@posts_router.get("/{post_id}", status_code=status.HTTP_200_OK, name="post_details")
async def get_post_by_id(request: Request, post_id: int, session: Annotated[AsyncSession, Depends(app_session)]):
    statement = await session.execute(
        select(Post).where(Post.id == post_id)
    )
    
    post = statement.scalars().first()
    
    if post:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            status_code=status.HTTP_200_OK,
            context={"post": post}
        )
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found"
    )    

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


# getting all the user posts here 
@posts_router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
async def get_user_posts(user_id: uuid.UUID, session: Annotated[AsyncSession, Depends(app_session)]):
    statement = await session.execute(
        select(User).where(User.id == user_id)
    )
    
    user = statement.scalars().first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # we will fetch all the posts by user 
    user_posts = await session.execute(
        select(Post).select(Post.user_id == user_id)
    )
    
    all_user_posts = user_posts.scalars().all()
    
    return all_user_posts