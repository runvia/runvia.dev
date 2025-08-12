from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select

from app.db import get_session
from app.models.cv import ExperienceItem
from app.schemas.cv import ExperienceCreate, ExperienceRead, ExperienceUpdate

router = APIRouter(
    prefix="",
    tags=["Admin"],
    responses={404: {'description': "Not Found"}},
)

@router.get("/", response_model=List[ExperienceRead])
def list_expreriences(*, session: Session = Depends(get_session)) -> List[ExperienceRead]:
    """
    Retrive all experience entries
    """
    experiences = session.exec(select(ExperienceItem)).all()
    return experiences


@router.post("/", response_model=ExperienceRead, status_code=status.HTTP_201_CREATED)
def create_experience(
    *, 
    experience: ExperienceCreate, 
    session: Session = Depends(get_session)
) -> ExperienceRead:
    """
    Create a new experience entry.
    """
    new_item = ExperienceItem(**experience.dict())

    session.add(new_item)
    session.commit()
    session.refresh(new_item)

    return new_item


@router.get("/{experience_id}", response_model=ExperienceRead)
def get_experience(
    *,
    experience_id: int, session: Session = Depends(get_session)
):
    """
    Get a single experience entry
    """
    item = session.get(ExperienceItem, experience_id)
    if not item:
        raise HTTPException(status_code=404, detail="Experience not found")
    return item


@router.put("/{experience_id}", response_model=ExperienceRead)
def update_experience(
    *,
    experience_id: int,
    experience: ExperienceUpdate,
    session: Session = Depends(get_session)
):
    """
    Update an existing experience entry.
    """
    db_item = session.get(ExperienceItem, experience_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Experience not found")

    update_data = experience.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)

    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@router.delete("/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_experience(
    *,
    experience_id: int,
    session: Session = Depends(get_session)
):
    """
    Deletes an existing experience entry.
    """
    db_item = session.get(ExperienceItem, experience_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Experience not found")
    session.delete(db_item)
    session.commit()
