from app.schemas.post_schemas import CreatePost
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.models.users import User
from app.models.posts import Post


class PostServices:
    
    # we will create the post here 
    async def create_new_post(self, post_data: CreatePost, session: AsyncSession):
        statement = await session.execute(
            select(User).where(User.id == post_data.user_id)
        )
        user = statement.scalars().first()
        if not user:
            return None
        else:
            post_dict = post_data.model_dump()
            new_post = Post(**post_dict)
            session.add(new_post)
            await session.commit()
            await session.refresh(new_post)
            return new_post
        