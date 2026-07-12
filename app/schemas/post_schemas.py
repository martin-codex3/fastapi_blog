from pydantic import BaseModel, Field, ConfigDict


class PostBase(BaseModel):

    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=50)


# for creating a new post 
class CreatePost(PostBase):
    pass

# for the created post response 
class PostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int