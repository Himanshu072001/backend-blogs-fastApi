from fastapi import Depends, Response, HTTPException, APIRouter
from .. import models
from ..database import  get_db 
from sqlalchemy.orm import Session
from ..schemas import CommentCreate, CommentResponse


router = APIRouter() # Create a router for comment-related endpoints

## ------------ Create new records in each table Operations ---------------    ##
@router.post("/create", status_code=201, response_model=CommentResponse)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    # Check if post exists
    post = db.query(models.Post).filter(models.Post.id == comment.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id '{comment.post_id}' not found")
    
    # Check if author exists
    author = db.query(models.User).filter(models.User.id == comment.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail=f"Author with id '{comment.author_id}' not found")
    
    # Create new comment
    db_comment = models.Comment(
        content=comment.content,
        post_id=comment.post_id,
        author_id=comment.author_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


# Sample endpoint to fetch all comments
@router.get("/all", status_code=200, response_model=list[CommentResponse])
def get_all_comments(db: Session = Depends(get_db)):
    comments = db.query(models.Comment).all()
    if not comments:
        return {"message": "No comments found"}
    return comments


# Get comment by ID
@router.get("/get/{comment_id}", status_code=200, response_model=CommentResponse)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail = f"Comment with id '{comment_id}' not found" )
    return comment


# Delete comment by ID
@router.delete("/delete/{comment_id}", status_code=204)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail=f"Comment with id '{comment_id}' not found")
    
    db.delete(db_comment)
    db.commit()
    return Response(status_code=204)