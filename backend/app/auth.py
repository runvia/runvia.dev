from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlmodel import Session, select
from app.db import engine
from passlib.context import CryptContext

from app.models.user import User

# Secret & algoritm
SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")


fake_users = {
    "niclas": {
        "username": "niclas",
        "hashed_password": pwd_context.hash("yourpassword"),
    }
}

def hash_password(plain: str) -> str:
    """Hash the provided password"""
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """Helper function to verify password"""
    return pwd_context.verify(plain, hashed)

def get_user_by_username(session: Session, username: str) -> Optional[User]:
    return session.exec(select(User).where(User.username == username)).first()


def authenticate_user(username: str, password: str) -> Optional[User]:
    """Function to authenticate the provided user"""
    with Session(engine) as session:
        user = get_user_by_username(session, username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None
        return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Creates the jwt token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_user_from_token(token: str) -> Optional[User]:
    """Decode JWT, then load user from db"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            return None
    except JWTError:
        return None
    with Session(engine) as session:
        return get_user_by_username(session, username)



async def get_current_user(token: str = Depends(oauth2_scheme)):
    """async function that gets the current user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username or username not in fake_users:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc
    return fake_users[username]