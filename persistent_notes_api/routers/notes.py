from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from persistent_notes_api.database import get_db
from persistent_notes_api.models import Note, User
from persistent_notes_api.schemas import NoteCreate, NoteUpdate, NoteResponse

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("/users/{user_id}", response_model=NoteResponse, status_code=201)
async def create_note(
    user_id: int,
    note_data: NoteCreate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    note = Note(
        title=note_data.title,
        content=note_data.content,
        user_id=user_id,
    )

    db.add(note)
    await db.commit()
    await db.refresh(note)

    return note


@router.get("/", response_model=list[NoteResponse])
async def get_notes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Note).order_by(Note.id)
    )
    return result.scalars().all()


@router.get("/users/{user_id}", response_model=list[NoteResponse])
async def get_user_notes(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Note)
        .join(Note.user)
        .where(User.id == user_id)
        .order_by(Note.id)
    )

    return result.scalars().all()


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Note).where(Note.id == note_id)
    )
    note = result.scalar_one_or_none()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return note


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int,
    note_data: NoteUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Note).where(Note.id == note_id)
    )
    note = result.scalar_one_or_none()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    updates = note_data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        if value is None:
            raise HTTPException(
                status_code=422,
                detail=f"{field} cannot be null",
            )
        setattr(note, field, value)

    await db.commit()
    await db.refresh(note)

    return note


@router.delete("/{note_id}", status_code=204)
async def delete_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Note).where(Note.id == note_id)
    )
    note = result.scalar_one_or_none()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    await db.delete(note)
    await db.commit()
