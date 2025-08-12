from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from sqlalchemy import desc


from app.db import get_session

from app.schemas.cv import CVDetail
from app.models.cv import CV, ExperienceItem, EducationItem



router = APIRouter()

@router.get("", response_model=CVDetail, tags=['CV'])
def get_cv(db: Session = Depends(get_session)):
    """Return my CV Data."""
    query = (
        select(CV)
        .options(
            selectinload(CV.experience),
            selectinload(CV.education),
            selectinload(CV.skills),
        )
        
    )
    cv = db.exec(query).one_or_none()
    if not cv:
        raise HTTPException(404, detail="CV not found")
    cv.experience.sort(key=lambda e: e.start, reverse=True)
    cv.education.sort(key=lambda e: e.start, reverse=True)
    return cv