from models.customer import Customer

import pytest

@pytest.fixture
def customer_without_id():
    return Customer(name="customer 1")

@pytest.fixture
def customer_with_id():
    return Customer(name="customer 2", customer_id="fixed-1")

def test_customer_name_is_title_cased(customer_without_id):
    assert customer_without_id.name == "Customer 1"

def test_customer_auto_generates_id(customer_with_id):
    assert isinstance(customer_with_id.customer_id, str)
    assert len(customer_with_id.customer_id) > 0

def test_customer_name_has_correct_id(customer_with_id):
    assert customer_with_id.name == "Customer 2"
    assert customer_with_id.customer_id == "fixed-1"

def test_two_customers_have_different_ids():
    customer_1 = Customer("Test 1")
    customer_2 = Customer("Test 2")
    assert customer_1.customer_id !=customer_2.customer_id