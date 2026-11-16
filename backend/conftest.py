# backend/conftest.py
import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

# Add the backend directory itself to sys.path so `import app` works
sys.path.insert(0, str(Path(__file__).parent.resolve()))

DB_URL = "sqlite://"
os.environ["DATABASE_URL"] = DB_URL
os.environ["SECRET_KEY"] = "test-secret-key-not-for-production"
os.environ["SESSION_SECRET_KEY"] = "test-secret-key-not-for-production"

# Imported after the env vars above: importing app.main reads the settings.
from app.db import get_session
from app.main import app


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        DB_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
