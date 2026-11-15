from sqlalchemy import Boolean, Column, String
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(String(150), unique=True, index=True, nullable=False)
    hashed_password: str
    is_active: bool = Field(default=True, sa_column=Column(Boolean, nullable=False))
    is_superuser: bool = Field(default=True, sa_column=Column(Boolean, nullable=False))
