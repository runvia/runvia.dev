from datetime import UTC, datetime, timedelta
from typing import Annotated

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session, select

from app.config import get_settings
from app.db import get_session
from app.models.user import User

# Secret & algoritm
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
MAX_PASSWORD_BYTES = 72

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def hash_password(plain: str) -> str:
    """Hash the provided password"""
    bytes_string = plain.encode("utf-8")
    if len(bytes_string) > MAX_PASSWORD_BYTES:
        raise ValueError(f"Password longer than {MAX_PASSWORD_BYTES} bytes")
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(bytes_string, salt)

    return password_hash.decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """Helper function to verify password"""
    plain_bytes = plain.encode("utf-8")
    if len(plain_bytes) > MAX_PASSWORD_BYTES:
        return False
    hashed_bytes = hashed.encode("utf-8")
    return bcrypt.checkpw(plain_bytes, hashed_bytes)


def get_user_by_username(session: Session, username: str) -> User | None:
    return session.exec(select(User).where(User.username == username)).first()


def authenticate_user(session: Session, username: str, password: str) -> User | None:
    """Function to authenticate the provided user"""
    user = get_user_by_username(session, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Creates the jwt token"""
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, get_settings().secret_key.get_secret_value(), algorithm=ALGORITHM
    )


def get_user_from_token(session: Session, token: str) -> User | None:
    """Decode JWT, then load user from db"""
    try:
        payload = jwt.decode(
            token, get_settings().secret_key.get_secret_value(), algorithms=[ALGORITHM]
        )
        username: str = payload.get("sub")
        if not username:
            return None
    except JWTError:
        return None
    return get_user_by_username(session, username)


async def get_current_user(
    session: Annotated[Session, Depends(get_session)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    """async function that gets the current user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    user = get_user_from_token(session, token)
    if not user:
        raise credentials_exception
    return user


def can_access_admin(user: User | None) -> bool:
    if not user:
        return False
    return user.is_superuser and user.is_active
