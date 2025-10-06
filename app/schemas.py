
from pydantic import BaseModel
from . import models


# Pydantic models for request bodies
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    user_name: str
    bio: str = None

# Pydantic model for creating a post
class PostCreate(BaseModel):
    title: str
    content: str
    author_id: int
    is_published: bool = True  


#Pydantic model for creating a comment
class CommentCreate(BaseModel):
    content: str
    post_id: int
    author_id: int



# Pydantic model for creating a like
class LikeCreate(BaseModel):
    post_id: int
    user_id: int 