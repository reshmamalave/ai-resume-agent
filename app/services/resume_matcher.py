"""Deterministic skill matching between a parsed resume and a job description.

Missing skills are reported as gaps rather than ever being added to the
resume's skill list - the agent must never claim experience the candidate
did not provide.
"""
from app.schemas.job_description import JobDescriptionAnalysis
from app.schemas.match import MatchResult
from app.schemas.resume import ParsedResume


def match_resume_to_job(resume: ParsedResume, job_analysis: JobDescriptionAnalysis) -> MatchResult:
    resume_skills = {s.lower().strip() for s in resume.skills if s.strip()}
    required = {s.lower().strip() for s in job_analysis.required_skills if s.strip()}
    preferred = {s.lower().strip() for s in job_analysis.preferred_skills if s.strip()}
    job_skills = required | preferred

    matching = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)
    extra = sorted(resume_skills - job_skills)

    total = len(job_skills) or 1
    match_score = round(len(matching) / total * 100, 2)

    recommendations = [
        f"Job requires '{skill}', which was not found on the resume. "
        "Only add it if you genuinely have this experience."
        for skill in missing
    ]

    return MatchResult(
        matching_skills=matching,
        missing_skills=missing,
        extra_skills=extra,
        match_score=match_score,
        recommendations=recommendations,
    )
