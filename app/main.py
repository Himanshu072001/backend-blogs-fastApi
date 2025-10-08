from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users, posts, comments, likes

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.title = "My FastAPI Application"
app.version = "1.0.0"
app.description = "This is a sample FastAPI application with custom metadata."


# Include routers for different modules
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(comments.router, prefix="/comments", tags=["Comments"])
app.include_router(likes.router, prefix="/likes", tags=["Likes"])


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

