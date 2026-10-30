from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    return {
        "application": "AI Resume Tailoring Agent",
        "status": "UP"
    }