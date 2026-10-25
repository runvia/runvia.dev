from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field, conint, ConfigDict
from app.models.cv import SkillCategory


class ExperienceCreate(BaseModel):
    """
    A Work Exprience entry in my cv
    """
    company: str
    role: str
    start: date
    end: Optional[date]
    description: str

    model_config = ConfigDict(from_attributes=True)

class ExperienceRead(ExperienceCreate):
    """
    What we return when we read an Experience
    """
    id: int


class EducationCreate(BaseModel):
    """
    An Education entry in my cv
    """
    institution: str
    degree: str
    start: date
    end: Optional[date]
    details: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class EducationRead(EducationCreate):
    """
    What we return when we read an Education
    """
    id: int


class SkillCreate(BaseModel):
    """
    A single skill entry for my CV.
    """
    name: str
    proficiency: str  # whatever you already use
    category: Optional[SkillCategory] = None
    years_experience: Optional[conint(ge=0)] = None
    last_used: Optional[date] = None
    tools: List[str] = Field(default_factory=list)
    description: Optional[str] = Field(default=None, max_length=300)

    model_config = ConfigDict(from_attributes=True)


class SkillRead(SkillCreate):
    """
    What we return when we read a skill
    """
    id: int


class CVDetail(BaseModel):
    id: int
    name: str
    title: str
    experience: List[ExperienceRead]
    education: List[EducationRead]
    skills: List[SkillRead]

    model_config = ConfigDict(from_attributes=True)
