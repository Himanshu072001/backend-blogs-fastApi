
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from . import models



##---------------------- User Models --------------------- ##

# Pydantic models for request bodies
class BaseUser(BaseModel):
    name: str
    email: str
    user_name: str
    bio: str = None

# Pydantic model for creating a user (Request body)
class UserCreate(BaseUser):
   password: str

#Pydantic model for reading a user (Response body)
class UserResponse(BaseUser):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # To work with ORM objects directly



##---------------------- Post Models --------------------- ##

# Pydantic base model for posts
class PostBase(BaseModel):
    title: str
    content: str
    author_id: int
    is_published: bool = True  


# Pydantic model for creating a post
class PostCreate(PostBase):
   pass # No additional fields needed for creation

# Pydantic model for reading a post (Response body)
class PostResponse(PostBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # To work with ORM objects directly


##---------------------- Comment Models --------------------- ##

class CommentBase(BaseModel):
    content: str
    post_id: int
    author_id: int


#Pydantic model for creating a comment
class CommentCreate(CommentBase):
    pass # No additional fields needed for creation

class CommentResponse(CommentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # To work with ORM objects directly 


##---------------------- Like Models --------------------- ##

class LikeBase(BaseModel):
    post_id: int
    user_id: int

# Pydantic model for creating a like
class LikeCreate(LikeBase):
    pass # No additional fields needed for creation

class LikeResponse(LikeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # To work with ORM objects directly

# Note: For simplicity, relationships (like nested user info in posts) are not included here.