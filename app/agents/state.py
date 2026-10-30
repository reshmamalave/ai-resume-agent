"""Shared state for the LangGraph resume-tailoring workflow."""
from typing import List, TypedDict

from app.schemas.job_description import JobDescriptionAnalysis
from app.schemas.match import MatchResult
from app.schemas.resume import ParsedResume


class AgentState(TypedDict, total=False):
    parsed_resume: ParsedResume
    job_text: str
    job_analysis: JobDescriptionAnalysis
    match_result: MatchResult
    optimized_resume: ParsedResume
    validation_errors: List[str]
    revision_count: int
