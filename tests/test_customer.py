# =============================================================================
# Tests for the Customer model.
# These are pure unit tests — no file I/O, no HTTP, just the class logic.
# =============================================================================

import pytest
from models.customer import Customer


@pytest.fixture
def customer():
    """A basic customer with an auto-generated ID."""
    return Customer(name="alice smith")

@pytest.fixture
def customer_with_id():
    """A customer created with a specific known ID (e.g. loaded from JSON)."""
    return Customer(name="bob jones", customer_id="fixed-99")


# -----------------------------------------------------------------------------
# CREATION TESTS
# -----------------------------------------------------------------------------

def test_customer_stores_name(customer):
    assert customer.name == "alice smith"

def test_customer_auto_generates_id(customer):
    # ID should be a non-empty string when none is provided.
    assert isinstance(customer.customer_id, str)
    assert len(customer.customer_id) > 0

def test_customer_uses_provided_id(customer_with_id):
    # When an ID is explicitly passed (e.g. loading from file), it must be kept.
    assert customer_with_id.customer_id == "fixed-99"

def test_two_customers_get_different_ids():
    # Each new customer should get a unique ID.
    c1 = Customer("alice")
    c2 = Customer("bob")
    assert c1.customer_id != c2.customer_id


# -----------------------------------------------------------------------------
# SERIALIZATION TESTS
# -----------------------------------------------------------------------------

def test_to_dict_contains_expected_keys(customer):
    data = customer.to_dict()
    assert set(data.keys()) == {"customer_id", "name"}

def test_to_dict_values_match_object(customer_with_id):
    data = customer_with_id.to_dict()
    assert data["customer_id"] == "fixed-99"
    assert data["name"] == "bob jones"

def test_from_dict_recreates_customer(customer_with_id):
    data = customer_with_id.to_dict()
    recreated = Customer.from_dict(data)

    assert recreated.customer_id == customer_with_id.customer_id
    assert recreated.name == customer_with_id.name
