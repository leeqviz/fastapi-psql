from uuid import UUID, uuid4

from sqlalchemy import MetaData, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.configs import settings


class Base(DeclarativeBase):
    __abstract__ = True
    
    metadata = MetaData(
        naming_convention=settings.postgres.naming_convention
    )
    
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4())