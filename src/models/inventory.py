from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Integer, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.created_at import Created_At_Mixin
from .mixins.updated_at import Updated_At_Mixin
from .mixins.uuid_pk import UUID_PK_Mixin

if TYPE_CHECKING:
    from src.models.character import Character
    from src.models.item import Item


class Inventory(UUID_PK_Mixin, Created_At_Mixin, Updated_At_Mixin, Base):
    __tablename__ = "inventories"

    character_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("characters.id", ondelete="CASCADE"),
        primary_key=True,
    )
    item_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("items.id", ondelete="RESTRICT"),
        primary_key=True,
    )
    quantity: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1, server_default="1"
    )
    equipped: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    attuned: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    notes: Mapped[str | None] = mapped_column(Text)

    character: Mapped["Character"] = relationship(back_populates="inventories")
    item: Mapped["Item"] = relationship(back_populates="inventories")
