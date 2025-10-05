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



## Create new records in each table Operations
# Pydantic models for request bodies
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    user_name: str
    bio: str = None

@app.post("/createUser", status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
   
    # Raise error if email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
     # Raise error if user_name already exists
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
    return db_user