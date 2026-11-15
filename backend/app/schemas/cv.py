from datetime import date

from pydantic import BaseModel, ConfigDict, Field, conint

from app.models.cv import SkillCategory


class ExperienceCreate(BaseModel):
    """
    A Work Exprience entry in my cv
    """

    company: str
    role: str
    start: date
    end: date | None
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
    end: date | None
    details: str | None

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
    category: SkillCategory | None = None
    years_experience: conint(ge=0) | None = None
    last_used: date | None = None
    tools: list[str] = Field(default_factory=list)
    description: str | None = Field(default=None, max_length=300)

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
    experience: list[ExperienceRead]
    education: list[EducationRead]
    skills: list[SkillRead]

    model_config = ConfigDict(from_attributes=True)
