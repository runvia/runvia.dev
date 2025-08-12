from decouple import config 
from sqlmodel import Session, create_engine

DATABASE_URL = config('DATABASE_URL')
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    """
    FastAPI dependency that yields a database session, and ensures it's closed
    after the request is finished.
    """
    with Session(engine) as session:
        yield session

