from typing import List
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db_config.sqlalchemy_async_connect import Base
from app.models.data.mixins import Timestamp


class Customer(Timestamp, Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    first_name: Mapped[str] = mapped_column(String(30))
    second_name: Mapped[str] = mapped_column(String(30))
    sur_name: Mapped[str] = mapped_column(String(30))
    cell_phone: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30))

    products: Mapped[List["Product"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan"
    )
