from fastapi import FastAPI, Depends, Response, HTTPException, APIRouter
from .. import models
from app.utils.auth import hash_password
from ..database import get_db 
from sqlalchemy.orm import Session
from ..schemas import UserCreate, UserResponse

router = APIRouter() # Create a router for user-related endpoints

@router.post("/create", status_code=201, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
   
    # Raise error if email already exists [Primary Key check]
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
     # Raise error if user_name already exists [Primary Key check]
    if db.query(models.User).filter(models.User.user_name == user.user_name).first():
        raise HTTPException(status_code=400, detail="User name already exists")
    
    # Hash the password before storing [Not Working Showing error]
    #--Error: password cannot be longer than 72 bytes,
    print(user.password )
    hassed_password = hash_password(user.password)
    print(hassed_password)
    user.password = hassed_password # Store hashed password
    

    # Create new user with hashed password
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


# Sample endpoint to fetch all users
@router.get("/all", status_code=200, response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        return {"message": "No users found"}
    return users


# Get user by ID
@router.get("/get/{user_id}", status_code=200, response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id '{user_id}' not found")
    return user


# Update user by ID
# TODO: Optional Params for update
@router.put("/update/{user_id}", status_code=200, response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    # Fetch the user to be updated
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User with id '{user_id}' not found")
    
    # Update user fields
    db_user.name = user.name
    db_user.email = user.email
    db_user.password = user.password
    db_user.user_name = user.user_name
    db_user.bio = user.bio

    db.commit()
    db.refresh(db_user)
    return db_user


# Delete user by ID
@router.delete("/delete/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User with id '{user_id}' not found")
    
    db.delete(db_user)
    db.commit()
    return Response(status_code=204)