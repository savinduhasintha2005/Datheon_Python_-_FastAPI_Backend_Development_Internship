from fastapi import FastAPI, HTTPException, Query, status
from .schemas import BookCreate, BookUpdate, BookResponse

app = FastAPI(
    title="Book Management API",
    description="A REST API to create, view, update, filter, and delete books.",
    version="1.0.0",
)

books: dict[int, dict] = {}
next_book_id = 1


@app.get("/", tags=["Home"])
def home():
    return {"message": "Welcome to the Book Management API"}

@app.get(
    "/books",
    response_model=list[BookResponse],
    tags=["Books"],
)
def get_books(
    title: str | None = Query(default=None),
    author: str | None = Query(default=None),
    genre: str | None = Query(default=None),
    min_price: float | None = Query(default=None, ge=0),
    max_price: float | None = Query(default=None, gt=0),
):
    if (
        min_price is not None
        and max_price is not None
        and min_price > max_price
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="min_price cannot be greater than max_price",
        )

    result = list(books.values())

    if title:
        result = [
            book for book in result
            if title.lower() in book["title"].lower()
        ]

    if author:
        result = [
            book for book in result
            if author.lower() in book["author"].lower()
        ]

    if genre:
        result = [
            book for book in result
            if genre.lower() in book["genre"].lower()
        ]

    if min_price is not None:
        result = [
            book for book in result
            if book["price"] >= min_price
        ]

    if max_price is not None:
        result = [
            book for book in result
            if book["price"] <= max_price
        ]

    return result

@app.get(
    "/books/{book_id}",
    response_model=BookResponse,
    tags=["Books"],
)
def get_book(book_id: int):
    book = books.get(book_id)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    return book

@app.post(
    "/books",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Books"],
)
def create_book(book: BookCreate):
    global next_book_id

    new_book = book.model_dump()
    new_book["id"] = next_book_id

    books[next_book_id] = new_book
    next_book_id += 1

    return new_book

@app.put(
    "/books/{book_id}",
    response_model=BookResponse,
    tags=["Books"],
)
def update_book(book_id: int, book: BookUpdate):
    existing_book = books.get(book_id)

    if existing_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    update_data = book.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    updated_book = {**existing_book, **update_data}
    books[book_id] = updated_book

    return updated_book

@app.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Books"],
)
def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    del books[book_id]
    return None
