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

    model_config = ConfigDict(from_attributes=True)
 

class BorrowBookRequest(BaseModel):
    customer_name: str
    customer_id: int