from .book import Book
class Inventory:
    def __init__(self):
        self.books = []

    def register_book(self, title, author, pages, price):
        new_Book=Book()
        new_Book.title=title
        new_Book.author=author
        new_Book.pages=pages
        new_Book.price=price

        self.books.append(new_Book)

        return new_Book
    
    def display_books(self):
        for book in self.books:
            print(book)

inventory=Inventory()
inventory.register_book("LORD OF THE RINGS", "J R R TOLKIEN", 1000, 50)
inventory.register_book("THE HOBBIT", "J R R TOLKIEN", 500, 30)

inventory.display_books()