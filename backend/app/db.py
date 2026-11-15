from sqlmodel import Session, create_engine

from app.config import get_settings

engine = create_engine(get_settings().database_url, echo=get_settings().database_echo)


def get_session():
    """
    FastAPI dependency that yields a database session, and ensures it's closed
    after the request is finished.
    """
    with Session(engine) as session:
        yield session
