from fastapi import APIRouter

router: APIRouter = APIRouter()

@router.get("", tags=["Health"])
def health_check():
    """
    Simple health check endpoint
    """
    return {"status": "OK"}

