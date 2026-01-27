from fastapi import FastAPI, HTTPException, status
from models.customers import Customers
from models.inventory import Inventory

from schemas.customer import CustomerCreate, CustomerResponse
from schemas.book import BookCreate, BookResponse, BorrowBookRequest
from typing import List

app = FastAPI(title="Library API")

inventory = Inventory()
customers = Customers()

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
    raise HTTPException(status_code=404, detail="Book not found")

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
            inventory.save_books()
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_book(book_id: str):
    for i, book in enumerate(inventory.books):
        if book.id == book_id:
            inventory.books.pop(i)
            inventory.save_books()
            return
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books/{book_id}/borrow", response_model=BookResponse)
def borrow_book (book_id: str, request: BorrowBookRequest):
    customer = customers.get_customer_by_id(request.customer_id)
    if inventory.lend_book_by_id(book_id, customer):
        book=inventory.get_book_by_id(book_id)
        return book
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book.is_available:
        raise HTTPException(status_code=400, detail="Book is already lent")
    

@app.post("/books/{book_id}/return", response_model=BookResponse)
def return_book(book_id:str):
    if inventory.return_book_by_id(book_id):
        book=inventory.get_book_by_id(book_id)
        return book

    book = inventory.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.is_available:
        raise HTTPException(status_code=400, detail="Book was not borrowed / already available")
    
@app.post("/customers/", response_model= CustomerResponse)
def create_customer(customer: CustomerCreate):
    newCustomer = customers.register_customer(customer.name)
    return newCustomer

@app.get("/customers/", response_model=List[CustomerResponse])
def get_customers():
    return customers.get_all_customers()

@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: str):
    customer = customers.get_customer_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
