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
        if(self._available):
            status="Available"
        else:
            status="Not Available"
        return f'{self._name} | {self._author} | {self._pages} | {self._price} | {status}'
    

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
    
    @property
    def is_available(self):
        return self.is_available
    
    @property
    def borrowed_by(self):
        return self.borrowed_by
    
    @book_edition.setter
    def book_edition(self, value):
        self._book_edition = value

    def borrow(self, customer):
        if not self.is_available:
            return False
        self.is_available = False
        self.borrowed_by = f"Customer ID: {customer.customer_id} | Name: {customer.name}"
        return True
    
    def return_book(self):
        if self.is_available:
            return False
        self.is_available = True
        self.borrowed_by = None
        return True