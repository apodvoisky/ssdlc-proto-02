from pydantic import BaseModel
from datetime import date


class CustomerReq(BaseModel):
    id: int
    first_name: str
    second_name: str
    sur_name: str
    cell_phone: str
    email: str
