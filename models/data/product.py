from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.data.customer_product import customer_product

from db_config.sqlalchemy_async_connect import Base


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    title = Column(String, unique=False, index=False)
    code = Column(String, unique=True, index=True)

    customers = relationship("Customer", secondary="customer_product", back_populates='products')
