# seed_skills.py
from datetime import date
from sqlmodel import SQLModel, Session, create_engine, select
from .models.cv import SkillItem, SkillCategory  # adjust import to your project
from .db import engine

def get_or_create(session: Session, item: SkillItem):
    existing = session.exec(
        select(SkillItem).where(SkillItem.name == item.name, SkillItem.category == item.category)
    ).first()
    if existing:
        # update lightweight fields if you want
        existing.proficiency = item.proficiency or existing.proficiency
        existing.years_experience = item.years_experience or existing.years_experience
        existing.last_used = item.last_used or existing.last_used
        existing.tools = item.tools or existing.tools
        existing.description = item.description or existing.description
        return existing
    session.add(item)
    return item

def main():
    SQLModel.metadata.create_all(engine)
    skills = [
        # Programming
        SkillItem(
            name="Python",
            category=SkillCategory.PROGRAMMING,
            proficiency="Advanced",
            years_experience=5,
            last_used=date(2025, 8, 1),
            tools=["Django", "FastAPI", "pytest", "mypy", "pylint", "flake8", "Black", "setuptools"],
            description="OOP, decorators, generators, packaging, testing, type checking.",
        ),
        SkillItem(
            name="JavaScript",
            category=SkillCategory.PROGRAMMING,
            proficiency="Intermediate",
            years_experience=3,
            last_used=date(2025, 8, 1),
            tools=["Node.js", "NPM", "ES Modules"],
            description="Core concepts, async (Promises/async-await), modular apps.",
        ),
        SkillItem(
            name="Git",
            category=SkillCategory.PROGRAMMING,
            proficiency="Advanced",
            years_experience=6,
            last_used=date(2025, 8, 1),
            tools=[],
            description="Branching, PR workflows, code reviews, tagging, releases.",
        ),

        # Networking & Automation
        SkillItem(
            name="Cisco DevNet Associate",
            category=SkillCategory.NETWORKING,
            proficiency="Certified",
            years_experience=2,
            last_used=date(2025, 7, 1),
            tools=["Cisco APIs", "Meraki", "Webex"],
            description="API automation, app deployment, network fundamentals.",
        ),
        SkillItem(
            name="Juniper JNCIA",
            category=SkillCategory.NETWORKING,
            proficiency="Certified",
            years_experience=2,
            last_used=date(2020, 6, 1),
            tools=["Junos"],
            description="Routing/switching fundamentals and troubleshooting.",
        ),
        SkillItem(
            name="Meraki Automation",
            category=SkillCategory.NETWORKING,
            proficiency="Advanced",
            years_experience=3,
            last_used=date(2025, 8, 1),
            tools=["Meraki Dashboard API", "Python"],
            description="Scripts for 300+ orgs, inventory lookups, clients, LLDP/CDP.",
        ),

        # Data Science
        SkillItem(
            name="Applied Data Science (Python)",
            category=SkillCategory.DATA_SCIENCE,
            proficiency="Intermediate",
            years_experience=2,
            last_used=date(2025, 5, 1),
            tools=["pandas", "scikit-learn", "matplotlib"],
            description="Predictive modeling, data prep, ML workflows.",
        ),

        # Architecture
        SkillItem(
            name="IT Architect (Foundation)",
            category=SkillCategory.ARCHITECTURE,
            proficiency="Certified",
            years_experience=1,
            last_used=date(2025, 8, 1),
            tools=["Architecture methods", "Processes"],
            description="Principles, methods, tasks; stakeholder collaboration.",
        ),

        # Other
        SkillItem(
            name="Packaging & Deployment",
            category=SkillCategory.OTHER,
            proficiency="Advanced",
            years_experience=4,
            last_used=date(2025, 8, 1),
            tools=["venv", "setuptools", "PyPI"],
            description="Project structure, versioning, releases to PyPI.",
        ),
        SkillItem(
            name="Testing & Quality",
            category=SkillCategory.OTHER,
            proficiency="Advanced",
            years_experience=4,
            last_used=date(2025, 8, 1),
            tools=["pytest", "unittest", "mypy", "pylint", "flake8", "Black", "logging"],
            description="Test suites, CI linting, type safety, structured logs.",
        ),
        SkillItem(
            name="Data Formats & Parsing",
            category=SkillCategory.OTHER,
            proficiency="Advanced",
            years_experience=5,
            last_used=date(2025, 8, 1),
            tools=["JSON", "YAML", "TOML", "CSV", "XML"],
            description="Serialization, config handling, interop.",
        ),
        SkillItem(
            name="Databases",
            category=SkillCategory.OTHER,
            proficiency="Intermediate",
            years_experience=3,
            last_used=date(2025, 7, 1),
            tools=["SQLite", "PostgreSQL", "SQLModel"],
            description="Modeling, migrations, simple integrations.",
        ),
        SkillItem(
            name="Embedded Systems (basics)",
            category=SkillCategory.OTHER,
            proficiency="Intermediate",
            years_experience=1,
            last_used=date(2024, 12, 1),
            tools=["Measurement & test"],
            description="Components, programming, measurement and testing.",
        ),
    ]

    with Session(engine) as session:
        for s in skills:
            get_or_create(session, s)
        session.commit()

if __name__ == "__main__":
    main()
