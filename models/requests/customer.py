from pydantic import BaseModel


class CustomerReq(BaseModel):
    first_name: str
    second_name: str
    sur_name: str
    cell_phone: str
    email: str
