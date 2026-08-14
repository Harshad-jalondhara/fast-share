from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv() # # .env file ki values load karo environment mein

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()