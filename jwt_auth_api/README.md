
# JWT Authentication API

A FastAPI project for user registration, login, JWT authentication, and protected endpoints.

## Features

- User registration
- Password hashing with Passlib and bcrypt
- JWT access token generation
- OAuth2 password authentication
- Protected routes using `Depends(get_current_user)`
- SQLite database with SQLAlchemy

## Folder Structure

```text
datheon_python_fastapi_internship/
│
├── jwt_auth_api/
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── database.py
│       ├── models.py
│       ├── schemas.py
│       ├── security.py
│       ├── dependencies.py
│       │
│       └── routers/
│           ├── __init__.py
│           ├── auth.py
│           └── users.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

```bash
pip install -r requirements.txt
```

Configure the `.env` file with your secret key and database settings.

## Run the Application

```bash
python -m uvicorn jwt_auth_api.app.main:app --reload
```

## API Documentation

Open Swagger UI:

http://127.0.0.1:8000/docs

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and get JWT token |
| GET | `/users/me` | Get current user profile |
| GET | `/users/protected` | Access protected data |
| GET | `/health` | Check API status |

## Authentication

Include the JWT access token in the Authorization header:

```text
Authorization: Bearer <your_access_token>
```

Protected endpoints require a valid token.
