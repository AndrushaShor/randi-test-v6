"""Database connection utilities with async SQLAlchemy support"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings
from app.database.models import Base


# Convert postgresql:// to postgresql+asyncpg:// for async support
DATABASE_URL = settings.DATABASE_URL.replace(
    "postgresql://",
    "postgresql+asyncpg://"
)

# Create async engine
engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=5,
    max_overflow=10,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


def get_engine() -> AsyncEngine:
    """Get the async SQLAlchemy engine
    
    Returns:
        AsyncEngine: The async database engine instance
    """
    return engine


async def init_db() -> None:
    """Initialize database tables
    
    Creates all tables defined in Base metadata.
    Use this for development/testing. In production, use Alembic migrations.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for database sessions
    
    Provides an async database session for each request.
    Automatically handles session lifecycle (commit/rollback/close).
    
    Usage:
        @app.get("/projects")
        async def get_projects(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(Project))
            return result.scalars().all()
    
    Yields:
        AsyncSession: An async SQLAlchemy session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
