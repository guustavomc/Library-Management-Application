from typing import Optional
from .customer import Customer

import json
import os


class Customers:
    def __init__(self):
        self.customers = []
        self.customers_file = "data/customers.json"
        self.load_customers()

    def load_customers(self):
        if os.path.exists(self.customers_file):
            with open(self.customers_file,'r') as f:
                data = json.load(f)
                self.customers = [Customer.from_dict(item) for item in data]
        else:
            os.makedirs(os.path.dirname(self.customers_file), exist_ok=True)

    def save_customers(self):
        with open(self.customers_file, 'w') as f:
            json.dump([customer.to_dict() for customer in self.customers], f, indent=4)

    def register_customer(self, name):
        customer = Customer(name)
        self.customers.append(customer)
        self.save_customers()
        return customer
    
    def get_customer_by_id(self, customer_id) -> Optional[Customer]:
        for cust in self.customers:
            if cust.customer_id == customer_id:
                return cust
        return None

    def get_all_customers(self):
        return self.customers