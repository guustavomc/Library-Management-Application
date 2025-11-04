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

    def current_book_quantity(self):
        return len(self.books)
    
    def available_books(self):
        print("Available books:")
        for book in self.books:
            if book.is_available:
                print(book)
    
    def return_book(self, book_title):
        book_title= book_title.title()
        for book in self.books:
            if book._name == book_title:
                if book.return_book():
                    print(f"Book '{book._name}' was returned successfully")
                    return True
                else:
                    print(f"Book '{book._name}' was already available")
                    return False

            else:
                print(f"Failed to locate '{book._name}' on inventory")
                return False
    
    def lend_book(self, book_title, customer):
        book_title= book_title.title()
        for book in self.books:
            if book._name==book_title:
                if book.borrow(customer):
                    print(f"Book '{book._name}' was lended to '{customer}'")
                    return True
                else:
                    print(f"Book '{book._name}' is already lended'")
                    return False
            else:
                print(f"Failed to locate '{book._name}' on inventory")
                return False