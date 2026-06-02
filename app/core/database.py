# database.py  —  engine, sesión y Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,   # reconecta si la conexión cayó
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    pass


# dependency para inyectar en cada endpoint
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()