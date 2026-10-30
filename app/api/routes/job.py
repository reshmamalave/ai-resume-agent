from fastapi import APIRouter, HTTPException

from app.schemas.job_description import JobDescriptionAnalysis, JobDescriptionRequest
from app.services.job_analyzer import analyze_job_description

router = APIRouter(prefix="/job", tags=["Job Description"])


@router.post("/analyze", response_model=JobDescriptionAnalysis)
async def analyze_job(payload: JobDescriptionRequest):
    try:
        return analyze_job_description(payload.text)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
