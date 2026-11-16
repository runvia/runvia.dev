from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.models.cv import CV, EducationItem, ExperienceItem, SkillItem


def test_no_cv_gives_404(client: TestClient):
    resp = client.get("/api/cv")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "CV not found"}


def test_a_cv_is_returned(client: TestClient, session: Session):
    cv = CV(name="Test Person", title="Developer")
    cv.education = [
        EducationItem(
            institution="Test University",
            degree="BSc",
            start=date(2015, 9, 1),
        )
    ]
    cv.experience = [
        ExperienceItem(
            company="Test Company",
            role="Developer",
            start=date(2015, 12, 1),
            description="Test description",
        )
    ]
    cv.skills = [
        SkillItem(
            name="uv",
            proficiency="advanced",
        )
    ]
    session.add(cv)
    session.commit()
    resp = client.get("/api/cv")
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Test Person"
    assert data["title"] == "Developer"
    assert len(data["experience"]) == 1
    assert len(data["education"]) == 1
    assert len(data["skills"]) == 1


def test_newest_experience_first(client: TestClient, session: Session):
    cv = CV(name="Test Person", title="Developer")
    cv.experience = [
        ExperienceItem(
            company="Test Company",
            role="Developer",
            start=date(2015, 12, 1),
            end=date(2018, 12, 1),
            description="Test description",
        ),
        ExperienceItem(
            company="Test Company2",
            role="Developer",
            start=date(2018, 12, 1),
            end=date(2022, 12, 1),
            description="Test description",
        ),
    ]
    session.add(cv)
    session.commit()
    resp = client.get("/api/cv")
    assert resp.status_code == 200
    assert resp.json()["experience"][0]["company"] == "Test Company2"


def test_tools_come_back_as_a_list(client: TestClient, session: Session):
    cv = CV(name="Test Person", title="Developer")
    cv.skills = [SkillItem(name="python", proficiency="advanced", tools=["uv", "ruff"])]
    session.add(cv)
    session.commit()
    resp = client.get("/api/cv")
    assert resp.status_code == 200
    assert resp.json()["skills"][0]["tools"] == ["uv", "ruff"]


def test_skill_without_proficiency(session: Session):
    cv = CV(name="Test Person", title="Developer")
    cv.skills = [
        SkillItem(
            name="uv",
        )
    ]
    session.add(cv)
    with pytest.raises(IntegrityError):
        session.commit()


def test_skill_with_negative_years(session: Session):
    cv = CV(name="Test Person", title="Developer")
    cv.skills = [SkillItem(name="uv", proficiency="advanced", years_experience=-1)]
    session.add(cv)
    with pytest.raises(IntegrityError):
        session.commit()
