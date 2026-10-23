
# Persistent Notes API

A REST API built with FastAPI, SQLAlchemy ORM, and SQLite. It manages users and notes with persistent database storage.

## Features

- Create and retrieve users
- Create, read, update, and delete notes
- One-to-many relationship between users and notes
- Asynchronous database sessions
- Data persists after server restarts
- Automatic API documentation with Swagger UI

## Folder Structure

```text
persistent_notes_api/
├── __init__.py
├── main.py
├── database.py
├── models.py
├── schemas.py
├── routers/
│   ├── __init__.py
│   ├── users.py
│   └── notes.py
├── requirements.txt
└── README.md
```

## Installation

```bash
pip install -r persistent_notes_api/requirements.txt
```

## Run the Application

From the project root directory:

```bash
python -m uvicorn persistent_notes_api.main:app --reload
```

## API Documentation

Open Swagger UI:

http://127.0.0.1:8000/docs

## Database

SQLite is used for persistent storage. The `notes.db` database and tables are created automatically when the application starts.
