from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID


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
    id: UUID

    class Config:
        orm_node = True


class Products(List[Product]):
    ...


class UserBase(BaseModel):
    first_name: str
    second_name: str
    sur_name: str
    cell_phone: str
    email: str

    class Config:
        orm_node = True


class User(UserBase):
    id: UUID

    class Config:
        orm_node = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    first_name: Optional[str]
    second_name: Optional[str]
    sur_name: Optional[str]
    cell_phone: Optional[str]
    email: Optional[str]


class CustomerBase(BaseModel):
    full_name: str
    short_name: str
    primary_contact: UUID
    secondary_contact: UUID


class CustomerUpdate(BaseModel):
    full_name: Optional[str]
    short_name: Optional[str]
    primary_contact: Optional[UUID]
    secondary_contact: Optional[UUID]


class Customer(CustomerBase):
    id: UUID
    products: List[Product]

    class Config:
        orm_node = True


class CustomerCreate(CustomerBase):
    ...


class Customers(List[Customer]):
    ...


class Token(BaseModel):
    access_token: str
    token_type: str
