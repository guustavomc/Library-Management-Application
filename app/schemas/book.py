# schemas/book.py
from pydantic import BaseModel, ConfigDict, field_serializer
from typing import Optional

class BookBase(BaseModel):
    name: str
    author: str
    pages: int
    price: float
    book_edition: int

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: str
    book_edition: int
    is_available: bool
    borrowed_by: Optional[str] = None

    @field_serializer('borrowed_by')
    def serialize_borrowed_by(self, value):
        if value is None:
            return None
        return f'Customer ID: {value.customer_id} | Name: {value.name}'
    
    model_config = ConfigDict(from_attributes=True)
 

class BorrowBookRequest(BaseModel):
    customer_name: str
    customer_id: int