from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db_config.sqlalchemy_async_connect import Base
from app.models.data.mixins import Timestamp

from app.infra.hashservice import HashService


class User(Timestamp, Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    first_name: Mapped[str] = mapped_column(String(30))
    second_name: Mapped[str] = mapped_column(String(30))
    sur_name: Mapped[str] = mapped_column(String(30))
    cell_phone: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30), unique=True)

    password: Mapped[str] = mapped_column(nullable=False)

    def verify_password(self, password: str) -> bool:
        return HashService.verify_password(password, self.password)
