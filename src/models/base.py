from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from src.configs import settings


class Base(DeclarativeBase):
    __abstract__ = True
    
    metadata = MetaData(
        naming_convention=settings.postgres.naming_convention
    )