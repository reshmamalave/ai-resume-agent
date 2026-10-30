from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.agents.workflow import run_agent_workflow
from app.schemas.job_description import JobDescriptionAnalysis
from app.schemas.match import MatchResult
from app.schemas.resume import ParsedResume

router = APIRouter(prefix="/agent", tags=["Agent"])


class AgentRunRequest(BaseModel):
    resume: ParsedResume
    job_text: str


class AgentRunResponse(BaseModel):
    job_analysis: JobDescriptionAnalysis
    match_result: MatchResult
    optimized_resume: ParsedResume
    validation_errors: list[str] = []


@router.post("/run", response_model=AgentRunResponse)
async def run_agent(payload: AgentRunRequest):
    try:
        result = run_agent_workflow(payload.resume, payload.job_text)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    return AgentRunResponse(
        job_analysis=result["job_analysis"],
        match_result=result["match_result"],
        optimized_resume=result["optimized_resume"],
        validation_errors=result.get("validation_errors", []),
    )
