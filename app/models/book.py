import uuid

class Book:
    def __init__(self, name, author, pages):
        self.id = str(uuid.uuid4())[:8]  # Simple ID
        self._name= name.title()
        self._author=author.title()
        self._pages=pages
        self._price=0
        self._book_edition=0
        self._available=True
        self._borrowed_by=None

    def __str__(self):
        status=""
        if(self._available):
            status="Available"
        else:
            status="Not Available"
        return f'{self._name} | {self._author} | {self._pages} | {self._price} | {status}'

    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        self._price = value

    @property
    def book_edition(self):
        return self._book_edition
    
    @property
    def is_available(self):
        return self._available
    
    @property
    def borrowed_by(self):
        return self._borrowed_by
    
    @book_edition.setter
    def book_edition(self, value):
        self._book_edition = value

    def borrow(self, person):
        if not self._available:
            return False
        self._available = False
        self._borrowed_by = person
        return True
    
    def return_book(self):
        if self._available:
            return False
        self._available = True
        self._borrowed_by = None
        return True