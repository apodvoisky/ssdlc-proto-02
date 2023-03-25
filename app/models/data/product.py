import uuid
from sqlalchemy import String, text
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey

from app.db_config.sqlalchemy_async_connect import Base

from app.models.data.mixins import Timestamp


class Product(Timestamp, Base):
    __tablename__ = "product"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=text('uuid_generate_v4()'))

    title: Mapped[str] = mapped_column(String(30))
    code: Mapped[str] = mapped_column(String(10))
    customer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("customer.id"))

    customer: Mapped["Customer"] = relationship(back_populates="products")
