import uuid

class Book:
    def __init__(self, name, author, pages):
        self.id = str(uuid.uuid4())[:8]  # Simple ID
        self._name= name.title()
        self._author=author.title()
        self._pages=pages
        self._price=0
        self._book_edition=0
        self.is_available=True
        self.borrowed_by=None

    def __str__(self):
        status=""
        if(self.is_available):
            status="Available"
        else:
            status="Not Available"
        return f'{self._name} by {self._author} ({self._pages} pages, ${self._price}, Edition {self._book_edition}) | {status} | Borrowed by: {self.borrowed_by or "None"}'

    @property
    def name(self):
        return self._name
    
    @property
    def author(self):
        return self._author
    
    @property
    def pages(self):
        return self._pages

    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        self._price = value

    @property
    def book_edition(self):
        return self._book_edition
    
    
    @book_edition.setter
    def book_edition(self, value):
        self._book_edition = value

    def borrow(self, customer):
        if not self.is_available:
            return False
        self.is_available = False
        self.borrowed_by = customer.customer_id
        return True
    
    def return_book(self):
        if self.is_available:
            return False
        self.is_available = True
        self.borrowed_by = None
        return True
    
    def to_dict(cls):
        return {
            "id": self.id,
            "name": self._name,
            "author": self._author,
            "pages": self._pages,
            "price": self._price,
            "book_edition": self._book_edition,
            "is_available": self._is_available,
            "borrowed_by": self._borrowed_by
        }
    
    @classmethod
    def from_dict(cls, data):
        book = cls(data["name"],data["author"],data["pages"])
        book.id = data["id"]
        book._price = data["price"]
        book._book_edition = data["book_edition"]
        book.is_available = data["is_available"]
        book.borrowed_by = data["borrowed_by"]
        return book
    
    def __str__(self):
        status = "Available" if self.is_available else "Not Available"
        borrowed = f"Borrowed by ID: {self.borrowed_by}" if self.borrowed_by else "None"
        return f'{self._name} | {self._author} | {self._pages} | {self._price} | {status} | {borrowed}'


