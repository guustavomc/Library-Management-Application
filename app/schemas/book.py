# schemas/book.py
from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    name: str
    author: str
    pages: int
    price: float

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    book_edition: int
    is_available: bool
    borrowed_by: Optional[str] = None

    class Config:
        orm_mode = True