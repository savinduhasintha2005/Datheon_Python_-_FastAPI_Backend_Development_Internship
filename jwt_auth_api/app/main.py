from fastapi import FastAPI
from jwt_auth_api.app.database import Base, engine
from jwt_auth_api.app.routers import auth, users

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="JWT Authentication API",
    description=(
        "User registration, login, JWT authentication, "
        "and protected routes"
    ),
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {
        "message": "JWT Authentication API is running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
