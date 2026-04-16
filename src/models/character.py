from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import ForeignKey, Integer, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base
from .mixins import Created_At_Mixin, Updated_At_Mixin, UUID_PK_Mixin

if TYPE_CHECKING:
    from src.models.background import Background
    from src.models.inventory import Inventory
    from src.models.race import Race
    from src.models.user import User

class Character(UUID_PK_Mixin, Created_At_Mixin, Updated_At_Mixin, Base):
    __tablename__ = "characters"

    user_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    race_id: Mapped[Optional[UUID]] = mapped_column(
        Uuid,
        ForeignKey("races.id", ondelete="SET NULL"),
    )
    background_id: Mapped[Optional[UUID]] = mapped_column(
        Uuid,
        ForeignKey("backgrounds.id", ondelete="SET NULL"),
    )
    
    user: Mapped["User"] = relationship(back_populates="characters")
    race: Mapped[Optional["Race"]] = relationship(back_populates="characters")
    background: Mapped[Optional["Background"]] = relationship(back_populates="characters")
    stat: Mapped[Optional["CharacterStat"]] = relationship(
        back_populates="character",
        uselist=False,
        cascade="all, delete-orphan",
    )
    inventories: Mapped[list["Inventory"]] = relationship(
        back_populates="character",
        cascade="all, delete-orphan",
    )
    
class CharacterStat(Created_At_Mixin, Updated_At_Mixin, Base):
    __tablename__ = "character_stats"
    
    strength: Mapped[int] = mapped_column(Integer, nullable=False)
    dexterity: Mapped[int] = mapped_column(Integer, nullable=False)
    constitution: Mapped[int] = mapped_column(Integer, nullable=False)
    intelligence: Mapped[int] = mapped_column(Integer, nullable=False)
    wisdom: Mapped[int] = mapped_column(Integer, nullable=False)
    charisma: Mapped[int] = mapped_column(Integer, nullable=False)
    
    character_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("characters.id", ondelete="CASCADE"),
        primary_key=True,
        unique=True,
    )

    character: Mapped["Character"] = relationship(back_populates="stat")