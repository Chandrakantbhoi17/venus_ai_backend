
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base,Session
from app.core.config import settings


connect_args = {}
if settings.DB_TYPE == "sqlite":
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URI,
    connect_args=connect_args,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Session:
    """Yields a new database session and ensures it's closed after request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
