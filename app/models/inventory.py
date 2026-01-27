from typing import Optional
from .book import Book

import json
import os

class Inventory:
    def __init__(self):
        self.books = []
        self.books_file = "data/books.json"
        self.load_books()

    def load_books(self):
        if os.path.exists(self.books_file):
            with open(self.books_file, 'r') as f:
                data = json.load(f)
                self.books = [Book.from_dict(item) for item in data]
        else:
            os.makedirs(os.path.dirname(self.books_file), exist_ok=True)  # Create data/ if needed

    def save_books(self):
        with open(self.books_file, 'w') as f:
            json.dump([book.to_dict() for book in self.books], f, indent=4)

    def register_book(self, name, author, pages, price, book_edition):
        new_book=Book(name, author, pages)
        new_book.price=price
        new_book.book_edition=book_edition
        self.books.append(new_book)
        self.save_books()
        return new_book
    
    def display_books(self):
        for book in self.books:
            print(f"{book.id} | {book}")

    def current_book_quantity(self):
        return len(self.books)
    
    def available_books(self):
        print("Available books:")
        for book in self.books:
            if book.is_available:
                print(book)
    
    def get_book_by_id(self, book_id) -> Optional[Book]:

        for book in self.books:
            if book.id == book_id:
                return book
        return None
    
    def return_book_by_id(self, book_id):
        book = self.get_book_by_id(book_id)

        if not book:
            return False
        if book.is_available:
            return False
        book.return_book()
        self.save_books()
        return True
    
    def lend_book_by_id(self, book_id, customer):
        book = self.get_book_by_id(book_id)

        if not book:
            return False
        if not book.is_available:
            return False
        book.borrow(customer)
        self.save_books()  
        return True