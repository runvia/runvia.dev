from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select

from app.db import get_session
from app.models.cv import EducationItem
from app.schemas.cv import EducationCreate, EducationRead, EducationUpdate

router = APIRouter(
    prefix="/admin/education",
    tags=["Admin"],
    responses={404: {'description': "Not Found"}},
)

@router.get("/", response_model=List[EducationRead])
def list_education(*, session: Session = Depends(get_session)) -> List[EducationRead]:
    """
    Retrive all education entries
    """
    educations = session.exec(select(EducationItem)).all()
    return educations


@router.post("/", response_model=EducationRead, status_code=status.HTTP_201_CREATED)
def create_education(
    *, 
    education: EducationCreate, 
    session: Session = Depends(get_session)
) -> EducationRead:
    """
    Create a new education entry.
    """
    new_item = EducationItem(**education.dict())

    session.add(new_item)
    session.commit()
    session.refresh(new_item)

    return new_item


@router.get("/{education_id}", response_model=EducationRead)
def get_education(
    *,
    education_id: int, session: Session = Depends(get_session)
):
    """
    Get a single education entry
    """
    item = session.get(EducationItem, education_id)
    if not item:
        raise HTTPException(status_code=404, detail="Education not found")
    return item


@router.put("/{education_id}", response_model=EducationRead)
def update_education(
    *,
    education_id: int,
    education: EducationUpdate,
    session: Session = Depends(get_session)
):
    """
    Update an existing education entry.
    """
    db_item = session.get(EducationItem, education_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Education not found")

    update_data = education.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)

    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@router.delete("/{education_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_education(
    *,
    education_id: int,
    session: Session = Depends(get_session)
):
    """
    Deletes an existing education entry.
    """
    db_item = session.get(EducationItem, education_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Education not found")
    session.delete(db_item)
    session.commit()
