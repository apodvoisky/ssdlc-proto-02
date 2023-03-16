from sqlalchemy import Column, Integer, String

from db_config.sqlalchemy_async_connect import Base


class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    first_name = Column(String, unique=False, index=False)
    second_name = Column(String, unique=False, index=False)
    sur_name = Column(String, unique=False, index=False)
    cell_phone = Column(String, unique=False, index=False)
    email = Column(String, unique=False, index=False)
