import uuid
from sqlalchemy import String, text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.infra.base import Base
from app.models.data.mixins import Timestamp

from app.infra.hashservice import HashService


class User(Timestamp, Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=text('uuid_generate_v4()'))

    first_name: Mapped[str] = mapped_column(String(30))
    second_name: Mapped[str] = mapped_column(String(30))
    sur_name: Mapped[str] = mapped_column(String(30))
    cell_phone: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30), unique=True)

    password: Mapped[str] = mapped_column(nullable=False)

    def verify_password(self, password: str) -> bool:
        return HashService.verify_password(password, self.password)
