import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
from dotenv import load_dotenv
from app.infrastructure.models import Base

load_dotenv()

# SSL CA certificate path
SSL_CA = "../../certs/ca.pem"

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    print("Error: DATABASE_URL environment variable is not set")
    sys.exit(1)

if not DATABASE_URL.endswith('?'):
    DATABASE_URL += '?'
else:
    DATABASE_URL += '&'
DATABASE_URL += f"ssl_ca={SSL_CA}&ssl_verify_cert=true"

engine = create_engine(DATABASE_URL, echo=True)
# Create all tables including the new user_stories table
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)