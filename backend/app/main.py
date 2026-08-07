# app/main.py

from fastapi import FastAPI, APIRouter, Depends
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

# your existing routers
from app.routers import health, auth, secret
from app.routers import cv as public_cv      # public CV endpoint
from app.routers.admin import (
    experience, education, skill, cv as admin_cv
)
from app.auth import get_current_user, hash_password

# SQLAdmin imports
from sqladmin import Admin, ModelView
from wtforms import PasswordField, StringField, validators
from app.admin_auth import JWTAdminAuth        # your AuthenticationBackend subclass
from app.db import engine
from app.models.cv import ExperienceItem, EducationItem, SkillItem, CV
from app.models.user import User
from app.startup import ensure_default_admin
from decouple import config

SESSION_SECRET_KEY = config("SESSION_SECRET_KEY")


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_default_admin()
    yield

app = FastAPI(title="Runvia.dev API", lifespan=lifespan, root_path="/api")

# 1) SessionMiddleware is required for SQLAdmin’s login sessions
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)

# 2) CORS (for your React app on localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://runvia.dev"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3) Mount the SQLAdmin UI *first*, on /admin
admin = Admin(
    app=app,
    engine=engine,
    authentication_backend=JWTAdminAuth(secret_key=SESSION_SECRET_KEY),
    base_url="/admin",
)

# Register each model by subclassing ModelView
class ExperienceAdmin(ModelView, model=ExperienceItem):
    column_list = [ExperienceItem.company, ExperienceItem.role, ExperienceItem.start, ExperienceItem.end]
    column_sortable_list = [ExperienceItem.start]
    column_searchable_list = [ExperienceItem.company]
    form_columns = [
        ExperienceItem.company,
        ExperienceItem.role,
        ExperienceItem.start,
        ExperienceItem.end,
        ExperienceItem.description,
        ExperienceItem.cv,
    ]
    form_ajax_refs = {"cv": {"fields": ("name", "title")}}

class EducationAdmin(ModelView, model=EducationItem):
    column_list = [EducationItem.institution, EducationItem.degree, EducationItem.start]
    column_sortable_list = [EducationItem.start]
    column_searchable_list = [EducationItem.degree]
    form_columns = [
        EducationItem.institution,
        EducationItem.degree,
        EducationItem.start,
        EducationItem.end,
        EducationItem.details,
        EducationItem.cv,
    ]
    form_ajax_refs = {"cv": {"fields": ("name", "title")}}

class SkillAdmin(ModelView, model=SkillItem):
    column_sortable_list = [SkillItem.proficiency]
    column_searchable_list = [SkillItem.name]
    column_list = [
        SkillItem.id,
        SkillItem.name,
        SkillItem.category,
        SkillItem.years_experience,
        SkillItem.last_used,
        SkillItem.tools,
    ]
    form_columns = [
        SkillItem.name,
        SkillItem.proficiency,
        SkillItem.category,
        SkillItem.years_experience,
        SkillItem.last_used,
        SkillItem.tools,
        SkillItem.description,
    ]

class CVAdmin(ModelView, model=CV):
    form_columns = ["name","title","experience","education","skills"]

    

class UserAdmin(ModelView, model=User):
    column_list = [User.username, User.is_active, User.is_superuser]
    form_columns = ["username", "hashed_password", "is_active", "is_superuser"]
    form_overrides = {"username": StringField, "hashed_password": PasswordField}
    form_args = {
        "username": {"label": "Username"},
        "hashed_password": {
            "label": "Password",
            "validators": [validators.Optional()],
            "description": "Leave blank to keep existing password.",
        },
    }

    async def on_model_change(self, data, model, is_created, request):
        if data.get("hashed_password"):
            data["hashed_password"] = hash_password(data["hashed_password"])

admin.add_view(ExperienceAdmin)
admin.add_view(EducationAdmin)
admin.add_view(SkillAdmin)
admin.add_view(CVAdmin)
admin.add_view(UserAdmin)

# 4) Now group your JSON API under /api
api_router = APIRouter()

# public endpoints
api_router.include_router(
    health.router,
    prefix="/health",
    tags=["health"],
)
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"]
)
api_router.include_router(
    secret.router,
    prefix="/secret", 
    tags=["secret"]
)
api_router.include_router(
    public_cv.router,
    prefix="/cv",
    tags=["public_cv"]
)

# admin CRUD endpoints, to be called by your React app via /api/admin/...
api_router.include_router(
    experience.router,
    prefix="/admin/experience",
    tags=["admin_experience"],
    dependencies=[Depends(get_current_user)]
)
api_router.include_router(
    education.router,
    prefix="/admin/education",
    tags=["admin_education"],
    dependencies=[Depends(get_current_user)]
)
api_router.include_router(
    skill.router,
    prefix="/admin/skill",
    tags=["admin_skill"],
    dependencies=[Depends(get_current_user)]
)
api_router.include_router(
    admin_cv.router,
    prefix="/admin/cv",
    tags=["admin_cv"],
    dependencies=[Depends(get_current_user)]
)

# attach the /api router
app.include_router(api_router)


