# schemas/book.py
from pydantic import BaseModel
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

    class Config:
        orm_mode = True