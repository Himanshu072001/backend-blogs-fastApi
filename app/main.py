from fastapi import FastAPI, Depends, Response, HTTPException
from . import models
from .database import engine, SessionLocal, get_db 
from sqlalchemy.orm import Session
from .schemas import UserCreate, PostCreate, CommentCreate, LikeCreate, UserResponse, PostResponse, CommentResponse, LikeResponse

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
@app.get("/allPosts", status_code=200, response_model=list[PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    if not posts:
        return {"message": "No posts found"}
    return posts

# Sample endpoint to fetch all users
@app.get("/allUsers", status_code=200, response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        return {"message": "No users found"}
    return users

# Sample endpoint to fetch all comments
@app.get("/allComments", status_code=200, response_model=list[CommentResponse])
def get_all_comments(db: Session = Depends(get_db)):
    comments = db.query(models.Comment).all()
    if not comments:
        return {"message": "No comments found"}
    return comments

# Sample endpoint to fetch all likes
@app.get("/allLikes", status_code=200 , response_model=list[LikeResponse])
def get_all_likes(db: Session = Depends(get_db)):
    likes = db.query(models.Like).all()
    if not likes:
        return {"message": "No likes found"}
    return likes



## ------------ Create new records in each table Operations ---------------    ##

@app.post("/createUser", status_code=201, response_model=UserResponse)
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

 


@app.post("/createPost", status_code=201, response_model=PostResponse)
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



@app.post("/createComment", status_code=201, response_model=CommentResponse)
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


@app.post("/createLike", status_code=201, response_model=LikeResponse)
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



## ---------------------- Get User & Post by ID Operations --------------------- ##

# Get user by ID
@app.get("/getUser/{user_id}", status_code=200, response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id '{user_id}' not found")
    return user

# Get post by ID
@app.get("/getPost/{post_id}", status_code=200, response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail = f"Post with id '{post_id}' not found" )
    return post

# Get comment by ID
@app.get("/getComment/{comment_id}", status_code=200, response_model=CommentResponse)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail = f"Comment with id '{comment_id}' not found" )
    return comment

# Get like by ID
@app.get("/getLike/{like_id}", status_code=200, response_model=LikeResponse)
def get_like(like_id: int, db: Session = Depends(get_db)):
    like = db.query(models.Like).filter(models.Like.id == like_id).first()
    if not like:
        raise HTTPException(status_code=404, detail = f"Like with id '{like_id}' not found" )
    return like 




## ---------------------- Update User & Post by ID Operations --------------------- ##

# Update user by ID
# TODO: Optional Params for update
@app.put("/updateUser/{user_id}", status_code=200, response_model=UserResponse)
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


# Update post by ID
@app.put("/updatePost/{post_id}", status_code=200, response_model=PostResponse)
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



## ---------------------- Delete User & Post by ID Operations --------------------- ##

# Delete user by ID
@app.delete("/deleteUser/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User with id '{user_id}' not found")
    
    db.delete(db_user)
    db.commit()
    return Response(status_code=204)


# Delete post by ID
@app.delete("/deletePost/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail=f"Post with id '{post_id}' not found")
    
    db.delete(db_post)
    db.commit()
    return Response(status_code=204)

# Delete comment by ID
@app.delete("/deleteComment/{comment_id}", status_code=204)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail=f"Comment with id '{comment_id}' not found")
    
    db.delete(db_comment)
    db.commit()
    return Response(status_code=204)

# Delete like by ID
@app.delete("/deleteLike/{like_id}", status_code=204)
def delete_like(like_id: int, db: Session = Depends(get_db)):
    db_like = db.query(models.Like).filter(models.Like.id == like_id).first()
    if not db_like:
        raise HTTPException(status_code=404, detail=f"Like with id '{like_id}' not found")
    
    db.delete(db_like)
    db.commit()
    return Response(status_code=204)