from fastapi import FastAPI, HTTPException, status
from models.inventory import Inventory
from models.customer import Customer
from schemas.book import BookCreate, BookResponse
from typing import List

app = FastAPI(title="Library API")

inventory = Inventory()

inventory.register_book("LORD OF THE RINGS", "J R R TOLKIEN", 1000, 50,1)
inventory.register_book("THE HOBBIT", "J R R TOLKIEN", 500, 30, 2)

@app.get("/books/", response_model=List[BookResponse])
def get_books(available: bool = None):
    books = inventory.books
    if available is not None:
        books = [b for b in books if b.is_available == available]
    return books

@app.get("/books/{book_id}", response_model=BookResponse)
def get_book_with_id(book_id: str):
    books = inventory.books
    for book in books:
        if book.id == book_id:
            return book

@app.post("/books/",response_model=BookResponse)
def create_book(book: BookCreate):
    new_book = inventory.register_book(book.name, book.author, book.pages, book.price, book.book_edition)
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

@app.delete("/books/{book_id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_book(book_id: str):
    for i, book in enumerate(inventory.books):
        if book.id == book_id:
            inventory.books.pop(i)
            return

@app.post("/books/{book_id}/borrow", response_model=BookResponse)
def borrow_book (book_id: str, customer_name: str, customer_id: int):
     customer = Customer(customer_name, customer_id)
     for book in inventory.books:
        if book.id == book_id:
            if inventory.lend_book(book._name, customer):
                return book
            raise HTTPException(status_code=400, detail="Book is already lent")
        raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books/{book_id}/return", response_model=BookResponse)
def return_book(book_id:str):
    for book in inventory.books:
        if book.id == book_id:
            if inventory.return_book(book._name):
                return book
            raise HTTPException(status_code=400, detail="Book was already available")
        raise HTTPException(status_code=404, detail="Book not found")
