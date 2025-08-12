from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db import get_session
from app.models.cv import CV, ExperienceItem, EducationItem, SkillItem
from app.schemas.cv import CVCreate, CVRead, CVUpdate, CVDetail

router = APIRouter(
    prefix="/admin/cv",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[CVRead])
def list_cvs(*, session: Session = Depends(get_session)):
    """List all CV records."""
    return session.exec(select(CV)).all()


@router.post("/", response_model=CVRead, status_code=status.HTTP_201_CREATED)
def create_cv(
    *,
    cv: CVCreate,
    session: Session = Depends(get_session),
) -> CVRead:
    """Create a new CV."""
    new_cv = CV(**cv.dict())
    session.add(new_cv)
    session.commit()
    session.refresh(new_cv)
    return new_cv


@router.get("/{cv_id}", response_model=CVDetail)
def get_cv_detailed(*, cv_id: int, session: Session = Depends(get_session)) -> CVDetail:
    """Fetch one CV by ID, returning nested experience, education, and skills."""
    db_cv = session.get(CV, cv_id)
    if not db_cv:
        raise HTTPException(status_code=404, detail="CV not found")

    experiences = session.exec(
        select(ExperienceItem).where(ExperienceItem.id.in_(db_cv.experience))   # pylint: disable=no-member
    ).all()
    educations = session.exec(
        select(EducationItem).where(EducationItem.id.in_(db_cv.education))      # pylint: disable=no-member
    ).all()
    skills = session.exec(
        select(SkillItem).where(SkillItem.id.in_(db_cv.skills))                 # pylint: disable=no-member
    ).all()

    return CVDetail(
        id=db_cv.id,
        name=db_cv.name,
        title=db_cv.title,
        experience=experiences,
        education=educations,
        skills=skills,
    )


@router.put("/{cv_id}", response_model=CVRead)
def update_cv(
    *,
    cv_id: int,
    cv: CVUpdate,
    session: Session = Depends(get_session),
) -> CVRead:
    """Update an existing CV."""
    db_cv = session.get(CV, cv_id)
    if not db_cv:
        raise HTTPException(status_code=404, detail="CV not found")

    update_data = cv.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_cv, field, value)

    session.add(db_cv)
    session.commit()
    session.refresh(db_cv)
    return db_cv


@router.delete("/{cv_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cv(*, cv_id: int, session: Session = Depends(get_session)):
    """Delete a CV."""
    db_cv = session.get(CV, cv_id)
    if not db_cv:
        raise HTTPException(status_code=404, detail="CV not found")
    session.delete(db_cv)
    session.commit()
