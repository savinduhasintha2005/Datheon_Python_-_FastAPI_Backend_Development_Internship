# Book Management API

A RESTful API built using **FastAPI, Pydantic, and Uvicorn** to manage books with CRUD operations, query filtering, and request validation.

## Folder Structure

```text
book_management_api/
│
├── __init__.py
├── main.py
├── schemas.py
└── requirements.txt
```

- `main.py` – API endpoints and CRUD operations.
- `schemas.py` – Pydantic models for request validation.
- `requirements.txt` – Required Python packages.
- `__init__.py` – Marks the folder as a Python package.

## Features

- Create, retrieve, update, and delete books.
- Filter books by title, author, genre, and price.
- Validate input using Pydantic.
- Handle errors with appropriate HTTP status codes.
- Interactive Swagger documentation.

## Technologies

- Python 3
- FastAPI
- Pydantic
- Uvicorn

## Installation

```bash
pip install -r requirements.txt
```

## Run the Application

Run from the project root directory:

```bash
python -m uvicorn book_management_api.main:app --reload
```

## API Documentation

Open Swagger UI in your browser:

http://127.0.0.1:8000/docs

