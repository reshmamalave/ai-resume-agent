from typing import List

from pydantic import BaseModel

from app.schemas.job_description import JobDescriptionAnalysis
from app.schemas.resume import ParsedResume


class MatchRequest(BaseModel):
    resume: ParsedResume
    job_analysis: JobDescriptionAnalysis


class MatchResult(BaseModel):
    matching_skills: List[str] = []
    # Gaps are flagged, never silently filled in with invented experience.
    missing_skills: List[str] = []
    extra_skills: List[str] = []
    match_score: float
    recommendations: List[str] = []
