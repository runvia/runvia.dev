# app/main.py

from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

# your existing routers
from app.routers import health, auth, secret
from app.routers import cv as public_cv      # public CV endpoint
from app.routers.admin import (
    experience, education, skill, cv as admin_cv
)

# SQLAdmin imports
from sqladmin import Admin, ModelView
from sqlmodel import create_engine
from app.admin_auth import JWTAdminAuth        # your AuthenticationBackend subclass
from app.db import DATABASE_URL
from app.models.cv import ExperienceItem, EducationItem, SkillItem, CV
from app.models.user import User
from app.startup import ensure_default_admin, create_skills


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_default_admin()
    # create_skills()
    yield

app = FastAPI(title="Runvia.dev API", lifespan=lifespan, root_path="/api")

# 1) SessionMiddleware is required for SQLAdmin’s login sessions
app.add_middleware(SessionMiddleware, secret_key="super-secret-cookie-key")

# 2) CORS (for your React app on localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3) Mount the SQLAdmin UI *first*, on /admin
engine = create_engine(DATABASE_URL, echo=True)
admin = Admin(
    app=app,
    engine=engine,
    authentication_backend=JWTAdminAuth(secret_key="super-secret-cookie-key"),
    base_url="/api/admin",
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
        ExperienceItem.cv_id,
    ]

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
        EducationItem.cv_id
    ]

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
    pass

class UserAdmin(ModelView, model=User):
    column_list = [User.username, User.is_active, User.is_superuser]
    form_columns = [User.username, User.hashed_password, User.is_active, User.is_superuser]

admin.add_view(ExperienceAdmin)
admin.add_view(EducationAdmin)
admin.add_view(SkillAdmin)
admin.add_view(CVAdmin)
admin.add_view(UserAdmin)

# 4) Now group your JSON API under /api
api_router = APIRouter()

# public endpoints
api_router.include_router(health.router,    prefix="/health", tags=["health"])
api_router.include_router(auth.router,      prefix="/auth",   tags=["auth"])
api_router.include_router(secret.router,    prefix="/secret", tags=["secret"])
api_router.include_router(public_cv.router, prefix="/cv",     tags=["public_cv"])

# admin CRUD endpoints, to be called by your React app via /api/admin/...
api_router.include_router(
    experience.router,
    prefix="/admin/experience",
    tags=["admin_experience"],
)
api_router.include_router(
    education.router,
    prefix="/admin/education",
    tags=["admin_education"],
)
api_router.include_router(
    skill.router,
    prefix="/admin/skill",
    tags=["admin_skill"],
)
api_router.include_router(
    admin_cv.router,
    prefix="/admin/cv",
    tags=["admin_cv"],
)

# attach the /api router
app.include_router(api_router)


