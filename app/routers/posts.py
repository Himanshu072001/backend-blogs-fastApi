from fastapi import  Depends, Response, HTTPException, APIRouter
from .. import models
from ..database import engine, SessionLocal, get_db 
from sqlalchemy.orm import Session
from ..schemas import PostCreate, PostResponse

router = APIRouter() # Create a router for post-related endpoints

@router.post("/create", status_code=201, response_model=PostResponse)
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


## Fetch all records from each table Operations
# Sample endpoint to fetch all posts
@router.get("/all", status_code=200, response_model=list[PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    if not posts:
        return {"message": "No posts found"}
    return posts


# Get post by ID
@router.get("/get/{post_id}", status_code=200, response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail = f"Post with id '{post_id}' not found" )
    return post



# Update post by ID
@router.put("/update/{post_id}", status_code=200, response_model=PostResponse)
def update_post(post_id: int, post: PostCreate, db: Session = Depends(get_db)):
    # Fetch the post to be updated
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail=f"Post with id '{post_id}' not found")
    
    # Update post fields
    db_post.title = post.title
    db_post.content = post.content
    db_post.author_id = post.author_id
    db_post.is_published = post.is_published

    db.commit()
    db.refresh(db_post)
    return db_post


# Delete post by ID
@router.delete("/delete/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail=f"Post with id '{post_id}' not found")
    
    db.delete(db_post)
    db.commit()
    return Response(status_code=204)