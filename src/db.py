
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.configs import settings
from src.models import Base


class DatabaseConnection:
    def __init__(
        self, 
        url: str, 
        echo: bool = False, 
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 5,
    ) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )
        
    async def init(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
    async def dispose(self) -> None:
        await self.engine.dispose()
        
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_maker() as session:
            yield session
            
postgresConnection = DatabaseConnection(
    url=settings.postgres.url,
    echo=settings.postgres.echo,
    echo_pool=settings.postgres.echo_pool,
    pool_size=settings.postgres.pool_size,
    max_overflow=settings.postgres.max_overflow,
)