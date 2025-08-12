from datetime import timedelta

from starlette.requests import Request
from sqladmin.authentication import AuthenticationBackend
from app.auth import get_user_from_token, authenticate_user, create_access_token


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
        user = authenticate_user(username, password)  # expects non-None strings
        if not user:
            return False

        token = create_access_token({"sub": user.username}, expires_delta=timedelta(hours=12))
        request.session["token"] = token
        return True
    
    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True
        
    async def authenticate(self, request: Request) -> bool: 
        token = request.session.get("token")
        if not token:
            return False
        user = get_user_from_token(token)
        return user is not None
