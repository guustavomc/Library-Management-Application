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

def test_get_book_with_id_return_not_found(client):
    book_created =client.post("/books/", json={"name": "Dune", "author": "Frank Herbert", "pages": 412, "price": 19.99, "book_edition": 1}).json()
    response = client.get(f"/books/fakeID")
    assert response.status_code == 404

# POST /books/

def test_create_book_return_created_books(client):
    response = client.post("/books/", json={"name": "Dune", "author": "Frank Herbert", "pages": 412, "price": 19.99, "book_edition": 1})
    assert response.status_code == 200
    assert response.json()["name"] == "Dune"

def test_create_book_contains_id(client):
    response = client.post("/books/", json={"name": "Dune", "author": "Frank Herbert", "pages": 412, "price": 19.99, "book_edition": 1})
    assert response.status_code == 200
    assert response.json()["id"] != None

# PUT /books/{book_id}

def test_update_book_returns_updated_data(client):
    created = client.post("/books/", json={"name": "Dune", "author": "Frank Herbert", "pages": 412, "price": 19.99, "book_edition": 1}).json()
    updated = client.put(f"/books/{created['id']}", json={"name": "Dune", "author": "Frank Herbert", "pages": 412, "price": 19.99, "book_edition": 2})
    assert updated.status_code == 200
    assert updated.json()["book_edition"] == 2

def test_update_book_returns_not_found(client):
    created = client.post("/books/", json={"name": "Dune", "author": "Frank Herbert", "pages": 412, "price": 19.99, "book_edition": 1}).json()
    updated = client.put("/books/fakeID", json={"name": "Dune", "author": "Frank Herbert", "pages": 412, "price": 19.99, "book_edition": 2})
    assert updated.status_code == 404

# DELETE /books/{book_id}
def test_delete_book_returns_no_content(client):
    created = client.post("/books/", json={"name": "Dune", "author": "Frank Herbert", "pages": 412, "price": 19.99, "book_edition": 1}).json()
    deleted = client.delete(f"/books/{created['id']}")
    assert deleted.status_code == 204

def test_delete_book_returns_not_found(client):
    created = client.post("/books/", json={"name": "Dune", "author": "Frank Herbert", "pages": 412, "price": 19.99, "book_edition": 1}).json()
    deleted = client.delete("/books/fakeID")
    assert deleted.status_code == 404

def test_delete_book_removes_from_book_list(client):
    created = client.post("/books/", json={"name": "Dune", "author": "Frank Herbert", "pages": 412, "price": 19.99, "book_edition": 1}).json()
    deleted = client.delete(f"/books/{created['id']}")
    response = client.get("/books/")
    assert response.status_code == 200
    assert len(response.json()) == 0