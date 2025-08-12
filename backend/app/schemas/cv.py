from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field, conint
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

    class Config:
        orm_mode = True

class ExperienceRead(ExperienceCreate):
    """
    What we return when we read an Experience
    """
    id: int


class ExperienceUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    start: Optional[date] = None
    end: Optional[date] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True



class EducationCreate(BaseModel):
    """
    An Education entry in my cv
    """
    institution: str
    degree: str
    start: date
    end: Optional[date]
    details: Optional[str]

    class Config:
        orm_mode = True

class EducationUpdate(BaseModel):
    """
    An Education entry in my cv
    """
    institution: Optional[str]
    degree: Optional[str]
    start: Optional[date]
    end: Optional[date]
    details: Optional[str]

    class Config:
        orm_mode = True

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

    class Config:
        orm_mode = True

class SkillUpdate(BaseModel):
    """
    A single skill entry for my CV.
    """
    name: Optional[str] = None
    proficiency: Optional[str] = None
    category: Optional[SkillCategory] = None
    years_experience: Optional[conint(ge=0)] = None
    last_used: Optional[date] = None
    tools: Optional[List[str]] = None
    description: Optional[str] = Field(default=None, max_length=300)

    class Config:
        orm_mode = True

class SkillRead(SkillCreate):
    """
    What we return when we read a skill
    """
    id: int

class CVCreate(BaseModel):
    """
    Data required to create a new CV record.
    """
    name: str
    title: str
    experience: List[int]        # list of ExperienceItem IDs
    education: List[int]         # list of EducationItem IDs
    skills: List[int]            # list of Skill IDs

    class Config:
        orm_mode = True


class CVRead(CVCreate):
    """
    What we return when reading a CV.
    """
    id: int


class CVUpdate(BaseModel):
    """
    Fields you can change on an existing CV.
    All are optional so you can update parts.
    """
    name: Optional[str] = None
    title: Optional[str] = None
    experience: Optional[List[int]] = None
    education: Optional[List[int]] = None
    skills: Optional[List[int]] = None

    class Config:
        orm_mode = True


class CVDetail(BaseModel):
    id: int
    name: str
    title: str
    experience: List[ExperienceRead]
    education: List[EducationRead]
    skills: List[SkillRead]

    class Config:
        orm_mode = True

