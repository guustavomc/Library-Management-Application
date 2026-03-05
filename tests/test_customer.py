from models.customer import Customer

import pytest

@pytest.fixture
def customer_without_id():
    return Customer(name="Customer 1")

@pytest.fixture
def customer_with_id():
    return Customer(name="Customer 2", customer_id="fixed-1")