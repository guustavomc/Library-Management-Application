from fastapi import FastAPI, HTTPException
from models.inventory import Inventory
from models.customer import Customer
from schemas.book import BookCreate, BookResponse
from typing import List

app = FastAPI(title="Library API")

inventory = Inventory()

inventory.register_book("LORD OF THE RINGS", "J R R TOLKIEN", 1000, 50)
inventory.register_book("THE HOBBIT", "J R R TOLKIEN", 500, 30)

@app.get("/books/", response_model=List[BookResponse])
def get_books(available: bool = None):
    books = inventory.books
    if available is not None:
        books = [b for b in books if b.is_available == available]
    return books

@app.post("/books/",response_model=BookResponse)
def create_book(book: BookCreate):
    new_book = inventory.register_book(book.name, book.author, book.pages, book.price)
    return new_book

@app.put("/books/{book_id}",response_model=BookResponse)
def update_book(book_id: str, book_update: BookCreate):
    for book in inventory.books:
        if book.id == book_id:
            book._name = book_update.name.title()
            book._author = book_update.author.title()
            book._pages = book_update.pages
            book._price = book_update.price
            book._book_edition = book_update.book_edition
            return book