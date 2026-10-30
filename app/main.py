from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.resume import router as resume_router
from app.api.routes.job import router as job_router
from app.api.routes.match import router as match_router
from app.api.routes.agent import router as agent_router
from app.api.routes.generate import router as generate_router
from app.core.config import settings

app = FastAPI(
    title="AI Resume Tailoring Agent",
    description="An AI agent that tailors resumes to job descriptions.",
    version="1.0.0"
)

app.include_router(health_router, prefix=settings.API_PREFIX)
app.include_router(resume_router, prefix=settings.API_PREFIX)
app.include_router(job_router, prefix=settings.API_PREFIX)
app.include_router(match_router, prefix=settings.API_PREFIX)
app.include_router(agent_router, prefix=settings.API_PREFIX)
app.include_router(generate_router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    return {"message": "Welcome to AI Resume Tailoring Agent"}