import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# If running locally, it connects to localhost:5432. 
# If running inside Docker later, we can pass "postgresql://...postgres:5432..." via env vars.
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://engine_user:engine_password@localhost:5432/job_engine_db"
)

# Initialize the SQLAlchemy Engine
engine = create_engine(DATABASE_URL)

# Create a session factory to be used in our API and Worker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)