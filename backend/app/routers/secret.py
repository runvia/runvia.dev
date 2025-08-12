from fastapi import APIRouter, Depends
from app.auth import get_current_user

router = APIRouter()

@router.get("/secret", dependencies=[Depends(get_current_user)])
def read_secret():
    return {"secret": "🔒 top-secret data"}