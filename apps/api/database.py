from os import getenv
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

host = getenv("DB_HOST", "localhost")
port = getenv("DB_PORT", "15432")

engine = create_engine(
    f"postgresql://postgres:password@{host}:{port}/postgres",
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: Any = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
