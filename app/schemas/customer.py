
from pydantic import BaseModel, ConfigDict


class CustomerCreate(BaseModel):
    name: str

class CustomerResponse(BaseModel):
    customer_id:str
    name: str
    model_config = ConfigDict(from_attributes=True)