"""Database configuration with async SQLAlchemy 2"""

import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

# Get database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+asyncpg://postgres:{os.getenv('DB_PASSWORD', 'postgres')}@"
    f"{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/"
    f"{os.getenv('DB_NAME', 'watch_tower')}"
)

# Create async engine factory
def get_engine():
    return create_async_engine(
        DATABASE_URL,
        echo=os.getenv("DEBUG", "False").lower() == "true",
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
    )

# Engine will be created when needed
engine = None

def get_session_factory():
    global engine
    if engine is None:
        engine = get_engine()
    return async_sessionmaker(
        engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )

# Base class for models
Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async database session"""
    async_session = get_session_factory()
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    """Initialize database tables"""
    global engine
    if engine is None:
        engine = get_engine()
    async with engine.begin() as conn:
        # Enable PostGIS extension
        await conn.execute("CREATE EXTENSION IF NOT EXISTS postgis")
        await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        
        # Create tables
        await conn.run_sync(Base.metadata.create_all)
