from typing import TYPE_CHECKING

from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.uuid_pk import UUID_PK_Mixin

if TYPE_CHECKING:
    from src.models.character import Character


class Race(UUID_PK_Mixin, Base):
    __tablename__ = "races"

    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    size: Mapped[str | None] = mapped_column(Text)
    speed: Mapped[int | None] = mapped_column(Integer)
    description: Mapped[str | None] = mapped_column(Text)

    characters: Mapped[list["Character"]] = relationship(
        back_populates="race",
        passive_deletes=True,
    )
