from sqlalchemy import Boolean, Column
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(max_length=150, unique=True, index=True, nullable=False)
    hashed_password: str
    is_active: bool = Field(default=True, sa_column=Column(Boolean, nullable=False))
    is_superuser: bool = Field(default=False, sa_column=Column(Boolean, nullable=False))
