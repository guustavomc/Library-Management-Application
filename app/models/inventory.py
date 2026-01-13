from typing import Optional
from .book import Book

class Inventory:
    def __init__(self):
        self.books = []

    def register_book(self, name, author, pages, price, book_edition):
        new_book=Book(name, author, pages)
        new_book.price=price
        new_book.book_edition=book_edition
        self.books.append(new_book)
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
        print(f"Book '{book._name}' was returned successfully")
        return True
    
    def lend_book_by_id(self, book_id, customer):
        book = self.get_book_by_id(book_id)

        if not book:
            return False
        if not book.is_available:
            return False
        book.borrow(customer)
        print(f"Book '{book._name}' was lended to '{customer}'")        
        return True