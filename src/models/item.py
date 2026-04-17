from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.created_at import Created_At_Mixin
from .mixins.updated_at import Updated_At_Mixin
from .mixins.uuid_pk import UUID_PK_Mixin

if TYPE_CHECKING:
    from src.models.inventory import Inventory


class Item(UUID_PK_Mixin, Created_At_Mixin, Updated_At_Mixin, Base):
    __tablename__ = "items"

    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    type: Mapped[str] = mapped_column(Text, nullable=False)
    rarity: Mapped[str | None] = mapped_column(Text)
    weight: Mapped[Decimal | None] = mapped_column(Numeric(8, 2))
    price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    description: Mapped[str | None] = mapped_column(Text)

    inventories: Mapped[list["Inventory"]] = relationship(
        back_populates="item",
        passive_deletes=True,
    )
