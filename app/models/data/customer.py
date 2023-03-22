from typing import List
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey

from app.db_config.sqlalchemy_async_connect import Base
from app.models.data.mixins import Timestamp
from app.models.data.user import User


class Customer(Timestamp, Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    full_name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    short_name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    primary_contact: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    secondary_contact: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    products: Mapped[List["Product"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan"
    )
