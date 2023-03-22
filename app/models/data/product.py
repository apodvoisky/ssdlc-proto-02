from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey

from app.db_config.sqlalchemy_async_connect import Base

from app.models.data.mixins import Timestamp


class Product(Timestamp, Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(String(30))
    code: Mapped[str] = mapped_column(String(10))
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))

    customer: Mapped["Customer"] = relationship(back_populates="products")
