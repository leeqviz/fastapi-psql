from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from src.utils import timestamp_with_tz


class Updated_At_Mixin:
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=timestamp_with_tz, 
        onupdate=timestamp_with_tz, 
        server_default=func.now()
    )