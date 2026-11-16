from sqlmodel import Session

from app.auth import authenticate_user, can_access_admin, hash_password
from app.models.user import User


def make_user(session, password, is_active=True, is_superuser=True):
    user = User(
        username="Test",
        hashed_password=hash_password(password),
        is_active=is_active,
        is_superuser=is_superuser,
    )
    session.add(user)
    session.commit()
    return user


def test_authenticate_user_correct_password(session: Session):
    make_user(session, "testing")
    user_result = authenticate_user(session, "Test", "testing")
    assert user_result is not None


def test_authenticate_user_wrong_password(session: Session):
    make_user(session, "testing")
    user_result = authenticate_user(session, "Test", "testing123")
    assert user_result is None


def test_authenticate_user_not_active(session: Session):
    make_user(session, "testing", is_active=False)
    user_result = authenticate_user(session, "Test", "testing")
    assert user_result is None


def test_user_active_and_superuser():
    user = User(username="Test", hashed_password="x", is_active=True, is_superuser=True)
    assert can_access_admin(user) is True


def test_user_active_and_not_superuser():
    user = User(
        username="Test",
        hashed_password="x",
        is_active=True,
        is_superuser=False,
    )
    assert can_access_admin(user) is False


def test_user_not_active_and_superuser():
    user = User(
        username="Test", hashed_password="x", is_active=False, is_superuser=True
    )
    assert can_access_admin(user) is False


def test_user_not_active_and_not_superuser():
    user = User(
        username="Test", hashed_password="x", is_active=False, is_superuser=False
    )
    assert can_access_admin(user) is False


def test_none_user_can_access_admin():
    assert can_access_admin(None) is False


def test_user_default():
    user = User(
        username="Test",
        hashed_password="x",
    )
    assert user.is_superuser is False
