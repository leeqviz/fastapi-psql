from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.connection import get_async_session, init_db
from src.db.models import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server is starting...")
    await init_db()
    yield
    print("server is stopping...")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(User)) 
    items = result.scalars().all()        
    return items
