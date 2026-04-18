from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base
from .mixins import Created_At_Mixin, Updated_At_Mixin, UUID_PK_Mixin

if TYPE_CHECKING:
    from src.models.user_role import UserRole


class Role(UUID_PK_Mixin, Created_At_Mixin, Updated_At_Mixin, Base):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    user_roles: Mapped[list["UserRole"]] = relationship(
        back_populates="role",
        cascade="all, delete-orphan",
    )
