from pydantic import BaseModel, Field, ConfigDict


class BookCreate(BaseModel):
    title: str = Field(
        ..., min_length=1, max_length=150
    )
    author: str = Field(
        ..., min_length=1, max_length=100
    )
    price: float = Field(
        ..., gt=0
    )
    published_year: int = Field(
        ..., ge=1000, le=2100
    )
    genre: str = Field(
        ..., min_length=1, max_length=50
    )


class BookUpdate(BaseModel):
    title: str | None = Field(
        default=None, min_length=1, max_length=150
    )
    author: str | None = Field(
        default=None, min_length=1, max_length=100
    )
    price: float | None = Field(
        default=None, gt=0
    )
    published_year: int | None = Field(
        default=None, ge=1000, le=2100
    )
    genre: str | None = Field(
        default=None, min_length=1, max_length=50
    )


class BookResponse(BookCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
