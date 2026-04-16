from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from src.utils import timestamp_with_tz

from . import Base


class User(Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=timestamp_with_tz, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=timestamp_with_tz, onupdate=timestamp_with_tz, server_default=func.now())
    
    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"
