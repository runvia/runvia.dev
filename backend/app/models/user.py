from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String, Boolean


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(String(150), unique=True, index=True, nullable=False)
    hashed_password: str
    is_active: bool = Field(default=True, sa_column=Column(Boolean, nullable=False))
    is_superuser: bool = Field(default=True, sa_column=Column(Boolean, nullable=False))
