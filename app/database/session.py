# app/database/session.py
"""
Database Session Configuration
##############################

Used for:

1. Creating the database engine
2. Configuring database sessions
3. Providing a database dependency for API routes

It ensures:
- Proper database connection management
- Automatic session closing
- Clean separation of database configuration

"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./addresses.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
