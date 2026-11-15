from datetime import date
from enum import Enum

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, SQLModel


class CVSkill(SQLModel, table=True):
    skill_id: int = Field(default=None, foreign_key="skillitem.id", primary_key=True)
    cv_id: int = Field(default=None, foreign_key="cv.id", primary_key=True)


class CV(SQLModel, table=True):
    """
    My CV
    """

    id: int | None = Field(default=None, primary_key=True)
    name: str
    title: str
    experience: list["ExperienceItem"] = Relationship(back_populates="cv")
    education: list["EducationItem"] = Relationship(back_populates="cv")
    skills: list["SkillItem"] = Relationship(back_populates="cvs", link_model=CVSkill)

    def __repr__(self):
        return self.name


class ExperienceItem(SQLModel, table=True):
    """
    A Work Experience entry in my cv
    """

    id: int | None = Field(default=None, primary_key=True)
    company: str
    role: str
    start: date
    end: date | None = None
    description: str

    cv_id: int = Field(default=None, foreign_key="cv.id", index=True)
    cv: CV | None = Relationship(back_populates="experience")


class EducationItem(SQLModel, table=True):
    """
    An Education entry in my cv
    """

    id: int | None = Field(default=None, primary_key=True)
    institution: str
    degree: str
    start: date
    end: date | None = None
    details: str | None = None

    cv_id: int = Field(default=None, foreign_key="cv.id", index=True)
    cv: CV | None = Relationship(back_populates="education")


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

    id: int | None = Field(default=None, primary_key=True)
    name: str  # e.g. "Python", "Docker", "React"
    proficiency: str | None = None
    category: SkillCategory | None = Field(default=None)
    years_experience: int | None = Field(default=None)
    last_used: date | None = None
    tools: list[str] = Field(
        default_factory=list,
        sa_column=Column(JSONB, nullable=False, server_default="[]"),
    )
    description: str | None = Field(default=None)
    cvs: list[CV] = Relationship(back_populates="skills", link_model=CVSkill)
