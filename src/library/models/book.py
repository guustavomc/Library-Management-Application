
class Book:
    def __init__(self, name, author, pages):
        self._name= name.title()
        self._author=author.title()
        self._pages=pages
        self._price=0
        self._book_edition=0

    def __str__(self):
        return f'{self._name} | {self._author} | {self._pages} | {self._price}'
    
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