# my_project/database/db_session.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings # We will create this file next

# The connection string for your PostgreSQL database
# Format: "postgresql://user:password@host:port/dbname"
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get a DB session in your endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()