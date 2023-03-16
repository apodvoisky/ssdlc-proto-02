from sqlalchemy import Column, Table, ForeignKey
from db_config.sqlalchemy_async_connect import Base

customer_product = Table('customer_product', Base.metadata,
                            Column('customer_id', ForeignKey('customer.id'), primary_key=True),
                            Column('product_id', ForeignKey('product.id'), primary_key=True)
)
