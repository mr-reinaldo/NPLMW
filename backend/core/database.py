from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine

from core.configs import settings


engine: AsyncEngine = create_async_engine(
    settings.DB_URL,
)


Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine,
)