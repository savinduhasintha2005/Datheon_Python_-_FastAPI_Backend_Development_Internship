from contextlib import asynccontextmanager
from fastapi import FastAPI
from persistent_notes_api.database import engine, Base
from persistent_notes_api.routers import users, notes


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(
    title="Persistent Notes API",
    description="FastAPI with SQLAlchemy ORM and SQLite",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(users.router)
app.include_router(notes.router)


@app.get("/")
async def root():
    return {
        "message": "Persistent Notes API is running",
        "docs": "/docs",
    }