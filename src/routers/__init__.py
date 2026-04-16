from fastapi import APIRouter

from src.configs import settings

from .users import users_router

api_router = APIRouter()

@api_router.get("/")
async def root():
    return {"message": settings.api.message}

api_router.include_router(users_router, prefix="/users", tags=["users"])