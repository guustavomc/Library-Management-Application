# Library API - FastAPI Project

## Overview

This is a **RESTful API** for a simple **library management system** built with **FastAPI** and **Python OOP**. It allows you to:

- Register books
- List all or available books
- Lend books to customers
- Return borrowed books

Made for studying OOP and REST API development on Python.

## Project Structure

```
library-management-application/
├── app/
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── book.py
│   │   ├── customer.py
│   │   ├── customerBase.py
│   │   └── inventory.py
│   └── schemas/
│       ├── __init__.py
│       ├── book.py
│       └── customer.py
├── data/
│   ├── books.json
│   └── customers.json
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_book.py
│   ├── test_customer.py
│   └── test_inventory.py
├── README.md
└── requirements.txt
```

## Features

| Endpoint | Method | Description |
|---|---|---|
| `GET /books/` | GET | List all books (`?available=true/false`) |
| `GET /books/{book_id}` | GET | Return book with ID |
| `POST /books/` | POST | Create a new book |
| `PUT /books/{book_id}` | PUT | Update book with ID |
| `DELETE /books/{book_id}` | DELETE | Delete book with ID |
| `POST /books/{book_id}/borrow` | POST | Lend book to customer |
| `POST /books/{book_id}/return` | POST | Return a borrowed book |
| `POST /customers/` | POST | Create a new customer |
| `GET /customers/` | GET | Return list of customers |
| `GET /customers/{customer_id}` | GET | Return customer with ID |

## Tech Stack

- **FastAPI** — Modern, fast web framework
- **Pydantic** — Data validation and settings
- **Uvicorn** — ASGI server
- **pytest** — Unit testing framework
- **Python 3.8+**

## Installation

1. Clone the project
```bash
git clone https://github.com/guustavomc/Library-Management-Application
cd Library-Management-Application
```

2. Create virtual environment (optional)
```bash
python -m venv venv
source venv/bin/activate     # Linux/Mac
# venv\Scripts\activate      # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the API
```bash
uvicorn main:app --reload
```
Server starts at: http://127.0.0.1:8000

**Interactive Docs**
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Running Tests

From the project root directory:

```bash
# Run all tests
pytest tests/

# Run with verbose output (shows each test name)
pytest tests/ -v

# Run a specific test file
pytest tests/test_book.py -v

# Stop at the first failure
pytest tests/ -x

# Run Tests with coverate
pytest --cov
```

### Test structure

| File | What it tests |
|---|---|
| `tests/test_book.py` | Book creation, borrow/return logic, serialization |
| `tests/test_customer.py` | Customer creation, ID generation, serialization |
| `tests/test_inventory.py` | Register, lend, return, file persistence |

## API Usage Examples

1. Create a Book
```bash
curl -X POST "http://127.0.0.1:8000/books/" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Harry Potter and the Deathly Hallows",
        "author": "J K Rowling",
        "pages": 700,
        "price": 100.0,
        "book_edition": 1
    }'
```

2. List Available Books
```bash
curl "http://127.0.0.1:8000/books/?available=true"
```

3. Borrow a Book
```bash
curl -X POST "http://127.0.0.1:8000/books/5e0bac82/borrow" \
    -H "Content-Type: application/json" \
    -d '{"customer_id": "a03be7a8"}'
```

4. Return a Book
```bash
curl -X POST "http://127.0.0.1:8000/books/5e0bac82/return"
```

## Next Steps (Future Improvements)

- SQLite/PostgreSQL with SQLAlchemy
- Customer CRUD API (update, delete)
- JWT Authentication
- Docker Support
