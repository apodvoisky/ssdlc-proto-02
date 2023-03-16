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
