from pydantic import BaseModel
from typing import List


class CustomerReqBase(BaseModel):
    first_name: str
    second_name: str
    sur_name: str
    cell_phone: str
    email: str


class CustomerReq(CustomerReqBase):
    id: int

    class Config:
        orm_node = True


class CustomersReq(BaseModel):
    __root__: List[CustomerReq]


class ProductReqBase(BaseModel):
    title: str
    code: str


class ProductReq(ProductReqBase):
    id: int
    class Config:
        orm_node = True


class ProductsReq(BaseModel):
    __root__: List[ProductReq]


class CustomerSchema(CustomerReq):
    products: List[ProductReqBase]


class ProductSchema(ProductReq):
    customers: List[CustomerReqBase]
