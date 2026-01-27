
import uuid


class Customer:

    def __init__(self, name):
        self._name = name
        self._customer_id = self.generate_id()  # Auto-generate if not provided

    def __str__(self):
        return f'Customer ID: {self._customer_id} | Name: {self._name}'
    
    def generate_id(self):
        return str(uuid.uuid4())[:8]
    
    @property
    def name(self):
        return self._name
    
    @property
    def customer_id(self):
        return self._customer_id
    
    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "name": self.name
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["customer_id"])
