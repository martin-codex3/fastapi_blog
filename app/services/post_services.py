from app.schemas.post_schemas import CreatePost
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.models.posts import Post


class PostServices:
    
    async def check_if_user_exists(self, post_data: CreatePost, session: AsyncSession):
        statement = await session.execute(
            select(Post).where(Post.id == post_data.user_id)
        )
        
        user_exists = statement.scalars().first()
        
        if user_exists:
            return True
        else:
            return False
        
    # we will create the post here 
    async def create_new_post(self, post_data: CreatePost, session: AsyncSession):
        user_exists = await self.check_if_user_exists(
            post_data=post_data,
            session = session
        )
        
        if not user_exists:
            return None
        else:
            post_dict = post_data.model_dump()
            new_post = Post(**post_dict)
            session.add(new_post)
            await session.commit()
            await session.refresh(new_post)
            return new_post
            
        