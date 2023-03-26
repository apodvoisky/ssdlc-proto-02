from datetime import datetime

from sqlalchemy.orm import declarative_mixin
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


@declarative_mixin
class Timestamp:
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
