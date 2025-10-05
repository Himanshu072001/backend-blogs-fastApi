# This file is responsible for:
# Connecting your FastAPI app to the PostgreSQL database using SQLAlchemy.
# Managing sessions (so you can query and commit safely).
# Exposing a helper dependency for other parts of the app to access the database.


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os   



# Create the SQLAlchemy engine (responsible for DB connection)
engine = create_engine(DATABASE_URL)

# Create a configured "SessionLocal" class (database session factory)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
Base = declarative_base()   

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  

