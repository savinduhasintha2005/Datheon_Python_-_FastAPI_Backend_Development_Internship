# FastAPI Background Jobs API

A containerized FastAPI microservice for background email notifications, webhook dispatching, and API rate limiting.

## Features

- FastAPI BackgroundTasks
- Email notifications using SMTP
- HTTP webhook dispatching
- Rate limiting with SlowAPI
- Multi-stage Dockerfile
- Docker Compose support
- Health check endpoint
- Swagger API documentation

## Project Structure

```text
background_jobs_api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── limiter.py
│   ├── schemas.py
│   └── tasks.py
├── .dockerignore
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Run with Docker

Create a `.env` file from `.env.example`, then run:

```bash
docker compose up --build -d
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| POST | `/send-email` | Schedule an email |
| POST | `/send-webhook` | Schedule a webhook |

## Documentation

Open http://localhost:8000/docs

## Notes

Without SMTP credentials, email notifications are logged in development mode. Background tasks run within the API process and are not durable across container restarts.
