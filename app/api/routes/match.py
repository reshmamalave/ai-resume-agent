from fastapi import APIRouter

from app.schemas.match import MatchRequest, MatchResult
from app.services.resume_matcher import match_resume_to_job

router = APIRouter(prefix="/match", tags=["Match"])


@router.post("/", response_model=MatchResult)
async def match_resume(payload: MatchRequest):
    return match_resume_to_job(payload.resume, payload.job_analysis)
