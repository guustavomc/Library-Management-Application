from .book import Book
class Inventory:
    def __init__(self):
        self.books = []

    def register_book(self, name, author, pages, price):
        new_Book=Book(name, author, pages)
        new_Book.price=price

        self.books.append(new_Book)

        return new_Book
    
    def display_books(self):
        for book in self.books:
            print(book)
