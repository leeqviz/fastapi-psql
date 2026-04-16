from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base
from .mixins import Created_At_Mixin, Updated_At_Mixin, UUID_PK_Mixin

if TYPE_CHECKING:
    from src.models.character import Character

class User(UUID_PK_Mixin, Created_At_Mixin, Updated_At_Mixin, Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    
    characters: Mapped[list["Character"]] = relationship(
        back_populates="users",
        cascade="all, delete-orphan",
    )
    
    def __str__ (self):
        return f"User(id={self.id}, name={self.name}, email={self.email}, password={self.password})"
    
    def __repr__ (self):
        return str(self)