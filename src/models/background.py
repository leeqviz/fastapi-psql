from typing import TYPE_CHECKING, Optional

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.uuid_pk import UUID_PK_Mixin

if TYPE_CHECKING:
    from src.models.character import Character
    
class Background(UUID_PK_Mixin, Base):
    __tablename__ = "backgrounds"

    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text)

    characters: Mapped[list["Character"]] = relationship(
        back_populates="background",
        passive_deletes=True,
    )