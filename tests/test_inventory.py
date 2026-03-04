# =============================================================================
# Tests for the Inventory class.
#
# The challenge with Inventory is that its __init__ reads from a JSON file.
# We need to isolate tests from the real data/books.json file.
#
# HOW WE SOLVE THIS — monkeypatching:
#   pytest has a built-in fixture called "monkeypatch" that lets you
#   temporarily replace a function or attribute during a test.
#   Here we use it to swap out the file path so Inventory reads/writes
#   to a temporary folder that gets deleted after each test.
#
# "tmp_path" is another built-in pytest fixture that gives you a fresh
# temporary directory for each test.
# =============================================================================

import json
import pytest
from models.inventory import Inventory
from models.customer import Customer


# -----------------------------------------------------------------------------
# FIXTURE — creates an Inventory backed by a temp file, not the real one
# -----------------------------------------------------------------------------

@pytest.fixture
def inventory(tmp_path, monkeypatch):
    """
    Returns an Inventory instance that reads/writes to a temp directory.
    This keeps tests isolated — they never touch data/books.json.
    """
    fake_books_file = tmp_path / "books.json"

    # We patch the __init__ so that self.books_file points to our temp file
    # instead of the real one.
    original_init = Inventory.__init__

    def patched_init(self):
        self.books = []
        self.books_file = fake_books_file
        self.load_books()

    monkeypatch.setattr(Inventory, "__init__", patched_init)
    return Inventory()


@pytest.fixture
def fake_customer():
    return Customer(name="Alice", customer_id="cust-01")


# -----------------------------------------------------------------------------
# REGISTER BOOK TESTS
# -----------------------------------------------------------------------------

def test_register_book_adds_to_list(inventory):
    inventory.register_book("Dune", "Frank Herbert", 412, 19.99, 1)
    assert len(inventory.books) == 1

def test_register_book_returns_correct_book(inventory):
    book = inventory.register_book("Dune", "Frank Herbert", 412, 19.99, 1)
    assert book.name == "Dune"
    assert book.author == "Frank Herbert"

def test_register_book_persists_to_file(inventory):
    # After registering, the JSON file should exist and contain the book.
    inventory.register_book("Dune", "Frank Herbert", 412, 19.99, 1)

    with open(inventory.books_file, "r") as f:
        data = json.load(f)

    assert len(data) == 1
    assert data[0]["name"] == "Dune"


# -----------------------------------------------------------------------------
# GET BOOK BY ID TESTS
# -----------------------------------------------------------------------------

def test_get_book_by_id_returns_correct_book(inventory):
    book = inventory.register_book("Dune", "Frank Herbert", 412, 19.99, 1)
    found = inventory.get_book_by_id(book.id)
    assert found is book  # same object, not just equal values

def test_get_book_by_id_returns_none_for_unknown_id(inventory):
    result = inventory.get_book_by_id("does-not-exist")
    assert result is None


# -----------------------------------------------------------------------------
# LEND BOOK TESTS
# -----------------------------------------------------------------------------

def test_lend_book_returns_true_on_success(inventory, fake_customer):
    book = inventory.register_book("Dune", "Frank Herbert", 412, 19.99, 1)
    result = inventory.lend_book_by_id(book.id, fake_customer)
    assert result is True

def test_lend_book_marks_book_unavailable(inventory, fake_customer):
    book = inventory.register_book("Dune", "Frank Herbert", 412, 19.99, 1)
    inventory.lend_book_by_id(book.id, fake_customer)
    assert book.is_available is False

def test_lend_book_returns_false_when_already_lent(inventory, fake_customer):
    book = inventory.register_book("Dune", "Frank Herbert", 412, 19.99, 1)
    inventory.lend_book_by_id(book.id, fake_customer)  # first borrow

    another_customer = Customer(name="Bob", customer_id="cust-02")
    result = inventory.lend_book_by_id(book.id, another_customer)  # second attempt
    assert result is False

def test_lend_book_returns_false_for_unknown_id(inventory, fake_customer):
    result = inventory.lend_book_by_id("ghost-id", fake_customer)
    assert result is False


# -----------------------------------------------------------------------------
# RETURN BOOK TESTS
# -----------------------------------------------------------------------------

def test_return_book_returns_true_on_success(inventory, fake_customer):
    book = inventory.register_book("Dune", "Frank Herbert", 412, 19.99, 1)
    inventory.lend_book_by_id(book.id, fake_customer)

    result = inventory.return_book_by_id(book.id)
    assert result is True

def test_return_book_makes_book_available_again(inventory, fake_customer):
    book = inventory.register_book("Dune", "Frank Herbert", 412, 19.99, 1)
    inventory.lend_book_by_id(book.id, fake_customer)
    inventory.return_book_by_id(book.id)

    assert book.is_available is True

def test_return_book_returns_false_when_not_borrowed(inventory):
    book = inventory.register_book("Dune", "Frank Herbert", 412, 19.99, 1)
    # Book was never borrowed, returning it should fail.
    result = inventory.return_book_by_id(book.id)
    assert result is False

def test_return_book_returns_false_for_unknown_id(inventory):
    result = inventory.return_book_by_id("ghost-id")
    assert result is False


# -----------------------------------------------------------------------------
# FILE PERSISTENCE TEST — load_books reads back what save_books wrote
# -----------------------------------------------------------------------------

def test_load_books_reads_saved_data(inventory):
    # Register a book (which saves to file), then reload from file.
    book = inventory.register_book("1984", "George Orwell", 328, 12.99, 3)

    # Create a fresh inventory pointing to the same file — simulates a restart.
    inventory2 = Inventory.__new__(Inventory)
    inventory2.books = []
    inventory2.books_file = inventory.books_file
    inventory2.load_books()

    assert len(inventory2.books) == 1
    assert inventory2.books[0].name == "1984"
    assert inventory2.books[0].id == book.id
