from sqlalchemy.ext.asyncio import create_async_engine

from src.config import settings
from src.db.models import Base

engine = create_async_engine(
    url=settings.database_url,
    echo=True
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
