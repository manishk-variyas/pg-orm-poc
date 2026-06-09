# database.py
# How to connect to the database.
# create_engine reads the database URL from settings.
# SessionLocal creates a new connection when you call it.
# get_db() is used by FastAPI to give each request a fresh connection.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
