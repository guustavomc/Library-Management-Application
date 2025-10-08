
class Book:
    def __init__(self, title='', author='', pages=0):
        self.title=title
        self.author=author
        self.pages=pages
        self.price=0

    def __str__(self):
        return f'{self.title} | {self.author} | {self.pages} | {self.price}'
    
