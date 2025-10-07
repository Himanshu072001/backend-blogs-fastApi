from fastapi import Depends, Response, HTTPException, APIRouter
from .. import models
from ..database import  get_db 
from sqlalchemy.orm import Session
from ..schemas import LikeCreate, LikeResponse

router = APIRouter() # Create a router for like-related endpoints


@router.post("/create", status_code=201, response_model=LikeResponse)
def create_like(like: LikeCreate, db: Session = Depends(get_db)):
    # Check if post exists
    post = db.query(models.Post).filter(models.Post.id == like.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id '{like.post_id}' not found")
    
    # Check if user exists
    user = db.query(models.User).filter(models.User.id == like.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id '{like.user_id}' not found")
    
    # Create new like
    db_like = models.Like(
        post_id=like.post_id,
        user_id=like.user_id
    )
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like


# Sample endpoint to fetch all likes
@router.get("/all", status_code=200 , response_model=list[LikeResponse])
def get_all_likes(db: Session = Depends(get_db)):
    likes = db.query(models.Like).all()
    if not likes:
        return {"message": "No likes found"}
    return likes


# Get like by ID
@router.get("/get/{like_id}", status_code=200, response_model=LikeResponse)
def get_like(like_id: int, db: Session = Depends(get_db)):
    like = db.query(models.Like).filter(models.Like.id == like_id).first()
    if not like:
        raise HTTPException(status_code=404, detail = f"Like with id '{like_id}' not found" )
    return like 


# Delete like by ID
@router.delete("/delete/{like_id}", status_code=204)
def delete_like(like_id: int, db: Session = Depends(get_db)):
    db_like = db.query(models.Like).filter(models.Like.id == like_id).first()
    if not db_like:
        raise HTTPException(status_code=404, detail=f"Like with id '{like_id}' not found")
    
    db.delete(db_like)
    db.commit()
    return Response(status_code=204)