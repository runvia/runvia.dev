from fastapi import APIRouter

router: APIRouter = APIRouter()

@router.get("/health", tags=["Health"])
def health_check():
    """
    Simple health check endpoint
    """
    return {"status": "OK"}

