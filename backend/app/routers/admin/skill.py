from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select

from app.db import get_session
from app.models.cv import SkillItem
from app.schemas.cv import SkillCreate, SkillRead, SkillUpdate

router = APIRouter(
    prefix="/admin/skill",
    tags=["Admin"],
    responses={404: {'description': "Not Found"}},
)

@router.get("/", response_model=List[SkillRead])
def list_skill(*, session: Session = Depends(get_session)) -> List[SkillRead]:
    """
    Retrive all skill entries
    """
    skills = session.exec(select(SkillItem)).all()
    return skills


@router.post("/", response_model=SkillRead, status_code=status.HTTP_201_CREATED)
def create_skill(
    *, 
    skill: SkillCreate, 
    session: Session = Depends(get_session)
) -> SkillRead:
    """
    Create a new skill entry.
    """
    new_item = SkillItem(**skill.dict())

    session.add(new_item)
    session.commit()
    session.refresh(new_item)

    return new_item


@router.get("/{skill_id}", response_model=SkillRead)
def get_skill(
    *,
    skill_id: int, session: Session = Depends(get_session)
):
    """
    Get a single skill entry
    """
    item = session.get(SkillItem, skill_id)
    if not item:
        raise HTTPException(status_code=404, detail="Skill not found")
    return item


@router.put("/{skill_id}", response_model=SkillRead)
def update_skill(
    *,
    skill_id: int,
    skill: SkillUpdate,
    session: Session = Depends(get_session)
):
    """
    Update an existing skill entry.
    """
    db_item = session.get(SkillItem, skill_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Skill not found")

    update_data = skill.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)

    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(
    *,
    skill_id: int,
    session: Session = Depends(get_session)
):
    """
    Deletes an existing skill entry.
    """
    db_item = session.get(SkillItem, skill_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Skill not found")
    session.delete(db_item)
    session.commit()
