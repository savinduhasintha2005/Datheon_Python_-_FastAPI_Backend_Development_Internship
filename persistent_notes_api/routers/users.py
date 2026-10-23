from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from persistent_notes_api.database import get_db
from persistent_notes_api.models import User
from persistent_notes_api.schemas import UserCreate, UserResponse, UserWithNotes

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    user = User(
        name=user_data.name,
        email=user_data.email,
    )

    db.add(user)

    try:
        await db.commit()
        await db.refresh(user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )

    return user


@router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).order_by(User.id))
    return result.scalars().all()


@router.get("/{user_id}", response_model=UserWithNotes)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    statement = (
        select(User)
        .options(selectinload(User.notes))
        .where(User.id == user_id)
    )

    result = await db.execute(statement)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user
