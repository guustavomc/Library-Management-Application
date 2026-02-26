
from pydantic import BaseModel


class CustomerCreate(BaseModel):
    name: str

class CustomerResponse(BaseModel):
    customer_id:str
    name: str