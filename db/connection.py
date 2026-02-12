"""
Database connection utilities for PostgreSQL
"""
import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool

from db.models import Base


# Database connection parameters from environment
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "agent")
DB_PASSWORD = os.getenv("DB_PASSWORD", "agent_dev")

# Construct connection string
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def get_engine(pool_size: int = 5, max_overflow: int = 10, echo: bool = False):
    """
    Create and return a SQLAlchemy engine.
    
    Args:
        pool_size: Number of connections to maintain in the pool
        max_overflow: Maximum number of connections to create beyond pool_size
        echo: If True, log all SQL statements
        
    Returns:
        SQLAlchemy engine instance
    """
    return create_engine(
        DATABASE_URL,
        pool_size=pool_size,
        max_overflow=max_overflow,
        echo=echo,
        pool_pre_ping=True,  # Verify connections before using them
    )


def get_session_factory(engine=None):
    """
    Create and return a session factory.
    
    Args:
        engine: SQLAlchemy engine (creates new one if None)
        
    Returns:
        SessionLocal factory
    """
    if engine is None:
        engine = get_engine()
    
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )


def init_db(engine=None):
    """
    Initialize database by creating all tables.
    
    Args:
        engine: SQLAlchemy engine (creates new one if None)
    """
    if engine is None:
        engine = get_engine()
    
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function for FastAPI to get database session.
    
    Yields:
        Database session
        
    Usage:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    SessionLocal = get_session_factory()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# For convenience - create a default engine and session factory
default_engine = get_engine()
SessionLocal = get_session_factory(default_engine)
