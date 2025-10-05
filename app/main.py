from fastapi import FastAPI, Depends, HTTPException
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

@app.get("/allPosts")
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found")
    return posts

