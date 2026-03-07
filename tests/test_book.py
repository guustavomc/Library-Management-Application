# =============================================================================
# HOW PYTEST WORKS (quick intro):
#
#   - Any function that starts with "test_" is automatically run by pytest.
#   - "assert" checks that something is true. If it's false, the test fails.
#   - pytest collects all test_*.py files and runs them for you.
#
#   Run all tests from the project root with:
#       pytest tests/
#
#   Run just this file:
#       pytest tests/test_book.py
#
#   Run with verbose output (shows each test name):
#       pytest tests/test_book.py -v
# =============================================================================

from models.book import Book


# -----------------------------------------------------------------------------
# FIXTURES
# A fixture is a reusable setup helper. Instead of creating a Book object in
# every single test, we create it once here and pass it as a parameter.
# pytest automatically calls the fixture and injects the result.
# -----------------------------------------------------------------------------
import pytest

@pytest.fixture
def available_book():
    """Returns a fresh Book that has not been borrowed."""
    return Book(name="the great gatsby", author="f. scott fitzgerald", pages=180)

@pytest.fixture
def borrowed_book():
    """Returns a Book that is already borrowed by a fake customer."""
    book = Book(name="1984", author="george orwell", pages=328)
    # We create a simple fake customer object just for the borrow() call.
    # This avoids needing to import Customer in a Book test.
    class FakeCustomer:
        customer_id = "abc123"
    book.borrow(FakeCustomer())
    return book


# -----------------------------------------------------------------------------
# CREATION TESTS — verify the Book is created with the right data
# -----------------------------------------------------------------------------

def test_book_title_is_title_cased(available_book):
    # Book.__init__ calls .title() on the name, so we check that here.
    assert available_book.name == "The Great Gatsby"

def test_book_author_is_title_cased(available_book):
    assert available_book.author == "F. Scott Fitzgerald"

def test_book_is_available_on_creation(available_book):
    assert available_book.is_available is True

def test_book_not_borrowed_on_creation(available_book):
    assert available_book.borrowed_by is None

def test_book_gets_an_id_on_creation(available_book):
    # The ID should be a non-empty string
    assert isinstance(available_book.id, str)
    assert len(available_book.id) > 0


# -----------------------------------------------------------------------------
# BORROW TESTS
# -----------------------------------------------------------------------------

def test_borrow_returns_true_when_available(available_book):
    class FakeCustomer:
        customer_id = "cust-01"

    result = available_book.borrow(FakeCustomer())
    assert result is True

def test_borrow_makes_book_unavailable(available_book):
    class FakeCustomer:
        customer_id = "cust-01"

    available_book.borrow(FakeCustomer())
    assert available_book.is_available is False

def test_borrow_records_customer_id(available_book):
    class FakeCustomer:
        customer_id = "cust-01"

    available_book.borrow(FakeCustomer())
    assert available_book.borrowed_by == "cust-01"

def test_borrow_returns_false_when_already_borrowed(borrowed_book):
    # Trying to borrow a book that is already lent out should fail.
    class AnotherCustomer:
        customer_id = "cust-99"

    result = borrowed_book.borrow(AnotherCustomer())
    assert result is False


# -----------------------------------------------------------------------------
# RETURN TESTS
# -----------------------------------------------------------------------------

def test_return_book_returns_true_when_borrowed(borrowed_book):
    result = borrowed_book.return_book()
    assert result is True

def test_return_book_makes_book_available(borrowed_book):
    borrowed_book.return_book()
    assert borrowed_book.is_available is True

def test_return_book_clears_borrowed_by(borrowed_book):
    borrowed_book.return_book()
    assert borrowed_book.borrowed_by is None

def test_return_book_returns_false_when_already_available(available_book):
    # Returning a book that was never borrowed should fail.
    result = available_book.return_book()
    assert result is False


# -----------------------------------------------------------------------------
# SERIALIZATION TESTS — to_dict / from_dict round-trip
# This is important because it's how data is saved to and loaded from JSON.
# -----------------------------------------------------------------------------

def test_to_dict_contains_expected_keys(available_book):
    data = available_book.to_dict()
    expected_keys = {"id", "name", "author", "pages", "price", "book_edition", "is_available", "borrowed_by"}
    assert set(data.keys()) == expected_keys

def test_from_dict_recreates_book_correctly(available_book):
    # Convert to dict, then rebuild from that dict, and compare fields.
    data = available_book.to_dict()
    recreated = Book.from_dict(data)

    assert recreated.id == available_book.id
    assert recreated.name == available_book.name
    assert recreated.author == available_book.author
    assert recreated.pages == available_book.pages
    assert recreated.is_available == available_book.is_available
    assert recreated.borrowed_by == available_book.borrowed_by
