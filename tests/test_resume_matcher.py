from app.schemas.job_description import JobDescriptionAnalysis
from app.schemas.resume import ParsedResume
from app.services.resume_matcher import match_resume_to_job


def test_match_identifies_gaps_without_inventing_skills():
    resume = ParsedResume(skills=["Python", "MySQL"], raw_text="...")
    job_analysis = JobDescriptionAnalysis(
        required_skills=["Python", "PostgreSQL"],
        preferred_skills=["Docker"],
        raw_text="...",
    )

    result = match_resume_to_job(resume, job_analysis)

    assert result.matching_skills == ["python"]
    assert "postgresql" in result.missing_skills
    assert "docker" in result.missing_skills
    # MySQL must never be silently treated as satisfying the PostgreSQL requirement.
    assert "mysql" not in result.missing_skills
    assert result.match_score == 33.33
