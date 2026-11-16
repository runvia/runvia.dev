from datetime import timedelta

from sqladmin.authentication import AuthenticationBackend
from sqlmodel import Session
from starlette.requests import Request

from app.auth import (
    authenticate_user,
    can_access_admin,
    create_access_token,
    get_user_from_token,
)
from app.db import engine


class JWTAdminAuth(AuthenticationBackend):
    def __init__(self, secret_key):
        super().__init__(secret_key=secret_key)

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        # 1) ensure we actually got values
        if not username or not password:
            return False

        # 2) now call your existing auth logic
        with Session(engine) as session:
            user = authenticate_user(session, username, password)
        if not can_access_admin(user):
            return False

        token = create_access_token(
            {"sub": user.username}, expires_delta=timedelta(hours=12)
        )
        request.session["token"] = token
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        with Session(engine) as session:
            user = get_user_from_token(session, token)
        return can_access_admin(user)
