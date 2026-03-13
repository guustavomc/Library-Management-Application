import pytest

from fastapi.testclient import TestClient

from main import app, inventory, customers

@pytest.fixture(autouse=True)
def reset_state(tmp_path, monkeypatch):
    inventory.books = []
    inventory.books_file = tmp_path/"books.json"

    customers.customers = []
    customers.customers_file = tmp_path/"customers.json"

@pytest.fixture
def client():
    return TestClient(app)

# GET /books/

def test_get_books_return_books(client):
    client.post("/books/", json={"name": "Dune", "author": "Frank Herbert", "pages": 412, "price": 19.99, "book_edition": 1})
    response = client.get("/books/")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_books_return_empty_list(client):
    client.post("/books/")
    response = client.get("/books/")
    assert response.status_code == 200
    assert len(response.json()) == 0

def test_get_books_return_available_books(client):
    client.post("/books/", json={"name": "Dune", "author": "Frank Herbert", "pages": 412, "price": 19.99, "book_edition": 1})
    response = client.get("/books/?available=true")
    assert response.status_code == 200
    assert len(response.json()) == 1

# GET /books/{book_id}

def test_get_book_with_id_return_book(client):
    book_created =client.post("/books/", json={"name": "Dune", "author": "Frank Herbert", "pages": 412, "price": 19.99, "book_edition": 1}).json()
    response = client.get(f"/books/{book_created["id"]}")
    assert response.status_code == 200
    assert response.json()["id"] == book_created["id"]
