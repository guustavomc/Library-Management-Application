
class Customer:

    def __init__(self, name, customer_id):
        self._name = name
        self._customer_id = customer_id

    def __str__(self):
        return f'Customer ID: {self._customer_id} | Name: {self._name}'