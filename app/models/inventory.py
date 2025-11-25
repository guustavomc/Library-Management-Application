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
            borrowed = book.borrowed_by._name if book.borrowed_by else None
            print(f"{book.id} | {book}")

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