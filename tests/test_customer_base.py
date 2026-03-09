import json
import pytest

from models.customerBase import CustomerBase
from models.customer import Customer

@pytest.fixture
def customerBase(tmp_path, monkeypatch):
    fake_customer_file = tmp_path/"customers.json"

    original_init = CustomerBase.__init__

    def patched_init(self):
        self.customers = []
        self.customers_file = fake_customer_file
        self.load_customers()

    monkeypatch.setattr(CustomerBase, "__init__", patched_init)
    return CustomerBase()

@pytest.fixture
def fake_customer():
    return Customer(name="Customer 1", customer_id="id-1")

def test_register_customer(customerBase):
    customerBase.register_customer("Test Customer")
    assert len(customerBase.customers) ==1

def test_register_customer_return_correct_customer(customerBase):
    customer = customerBase.register_customer("Test Customer")
    assert customer.name == "Test Customer"

def test_register_customer_persists_to_file(customerBase):
    customerBase.register_customer("Test Customer")

    with open(customerBase.customers_file,"r") as f:
        data = json.load(f)
    
    assert len(data) == 1
    assert data[0]["name"] == "Test Customer"

def test_get_customer_by_id(customerBase):
    customer = customerBase.register_customer("Test Customer")
    data = customerBase.get_customer_by_id(customer.customer_id)
    assert data is customer

def test_get_customer_by_id_customer_unknown(customerBase):
    data = customerBase.get_customer_by_id("Test")
    assert data is None