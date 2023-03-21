from pydantic import BaseModel
from typing import List, Optional


class ProductBase(BaseModel):
    title: str
    code: str
    customer_id: int


class ProductUpdate(BaseModel):
    title: Optional[str]
    code: Optional[str]
    customer_id: Optional[int]


class ProductCreate(ProductBase):
    ...


class Product(ProductBase):
    id: int

    class Config:
        orm_node = True


class Products(List[Product]):
    ...


class CustomerBase(BaseModel):
    first_name: str
    second_name: str
    sur_name: str
    cell_phone: str
    email: str


class CustomerUpdate(BaseModel):
    first_name: Optional[str]
    second_name: Optional[str]
    sur_name: Optional[str]
    cell_phone: Optional[str]
    email: Optional[str]

class Customer(CustomerBase):
    id: int
    products: List[Product]

    class Config:
        orm_node = True


class CustomerCreate(CustomerBase):
    ...


class Customers(List[Customer]):
    ...