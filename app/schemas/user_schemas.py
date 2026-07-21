from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
import uuid

class UserBaseSchema(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr
   
# for creating a new user account 
class CreateUserSchema(UserBaseSchema):
    profile_image: str
    
# for the user response
class UserResponseSchema(UserBaseSchema):
    
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    profile_image: str | None
    image_path: str
    posted_at: datetime