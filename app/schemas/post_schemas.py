from pydantic import BaseModel, Field, ConfigDict
import uuid
from app.schemas.user_schemas import UserResponseSchema

class PostBase(BaseModel):

    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=50)


# for creating a new post 
class CreatePost(PostBase):
    user_id: uuid.UUID #Temporary

# for the created post response 
class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: uuid.UUID
    author: UserResponseSchema
    date_posted: str