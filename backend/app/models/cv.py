from typing import Optional, List
from enum import Enum
from datetime import date
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB


class CVSkill(SQLModel, table=True):
    skill_id: int = Field(default=None, foreign_key="skillitem.id", primary_key=True)
    cv_id: int = Field(default=None, foreign_key="cv.id", primary_key=True)


class CV(SQLModel, table=True):
    """
    My CV
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    title: str
    experience: List["ExperienceItem"] = Relationship(back_populates='cv')
    education: List["EducationItem"] = Relationship(back_populates='cv')
    skills: List["SkillItem"] = Relationship(back_populates="cvs", link_model=CVSkill)

    def __repr__(self):
        return self.name



class ExperienceItem(SQLModel, table=True):
    """
    A Work Experience entry in my cv
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    company: str
    role: str
    start: date
    end: Optional[date] = None
    description: str
    
    cv_id: int = Field(default=None, foreign_key="cv.id", index=True)
    cv: Optional[CV] = Relationship(back_populates="experience")
    

class EducationItem(SQLModel, table=True):
    """
    An Education entry in my cv
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    institution: str
    degree: str
    start: date
    end: Optional[date] = None
    details: Optional[str] = None

    cv_id: int = Field(default=None, foreign_key="cv.id", index=True)
    cv: Optional[CV] = Relationship(back_populates="education")


class SkillCategory(str, Enum):
    PROGRAMMING = "Programming"
    NETWORKING = "Networking"
    DATA_SCIENCE = "Data Science"
    ARCHITECTURE = "Architecture"
    OTHER = "Other"


class SkillItem(SQLModel, table=True):
    """
    A single skill entry for my CV.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str                # e.g. "Python", "Docker", "React"
    proficiency: Optional[str] = None
    category: Optional[SkillCategory] = Field(default=None)
    years_experience: Optional[int] = Field(default=None)
    last_used: Optional[date] = None
    tools: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSONB, nullable=False, server_default="[]"),
    )
    description: Optional[str] = Field(default=None)
    cvs: List[CV] = Relationship(back_populates="skills", link_model=CVSkill)



