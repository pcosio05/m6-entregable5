import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
from dotenv import load_dotenv
from app.infrastructure.models import Base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    print("Error: DATABASE_URL environment variable is not set")
    sys.exit(1)

engine = create_engine(DATABASE_URL, echo=True)
# Create all tables including the new user_stories table
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)