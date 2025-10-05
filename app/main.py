from fastapi import FastAPI, Depends, Response, HTTPException
from pydantic import BaseModel
from . import models
from .database import engine, SessionLocal, get_db 
from sqlalchemy.orm import Session

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.title = "My FastAPI Application"
app.version = "1.0.0"
app.description = "This is a sample FastAPI application with custom metadata."

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}



## Fetch all records from each table Operations
# Sample endpoint to fetch all posts
@app.get("/allPosts")
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    if not posts:
        return {"message": "No posts found"}
    return posts

# Sample endpoint to fetch all users
@app.get("/allUsers")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        return {"message": "No users found"}
    return users

# Sample endpoint to fetch all comments
@app.get("/allComments")
def get_all_comments(db: Session = Depends(get_db)):
    comments = db.query(models.Comment).all()
    if not comments:
        return {"message": "No comments found"}
    return comments

# Sample endpoint to fetch all likes
@app.get("/allLikes")
def get_all_likes(db: Session = Depends(get_db)):
    likes = db.query(models.Like).all()
    if not likes:
        return {"message": "No likes found"}
    return likes



## ------------ Create new records in each table Operations ---------------    ##
# Pydantic models for request bodies
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    user_name: str
    bio: str = None

@app.post("/createUser", status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
   
    # Raise error if email already exists [Primary Key check]
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
     # Raise error if user_name already exists [Primary Key check]
    if db.query(models.User).filter(models.User.user_name == user.user_name).first():
        raise HTTPException(status_code=400, detail="User name already exists")
    
    # Create new user
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=user.password,
        user_name=user.user_name,
        bio=user.bio
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return  db_user


# Pydantic model for creating a post
class PostCreate(BaseModel):
    title: str
    content: str
    author_id: int
    is_published: bool = True   


@app.post("/createPost", status_code=201)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    # Check if author exists
    author = db.query(models.User).filter(models.User.id == post.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail=f"Author with id '{post.author_id}' not found")
    
    # Create new post
    db_post = models.Post(
        title=post.title,
        content=post.content,
        author_id=post.author_id,
        is_published=post.is_published
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


## ---------------------- Get User & Post by ID Operations --------------------- ##

# Get user by ID
@app.get("/getUser/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id '{user_id}' not found")
    return user

# Get post by ID
@app.get("/getPost/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail = f"Post with id '{post_id}' not found" )
    return post


## ---------------------- Update User & Post by ID Operations --------------------- ##