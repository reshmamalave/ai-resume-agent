from app.services.job_analyzer import analyze_job_description

JOB_TEXT = """Senior Backend Engineer

Responsibilities:
- Design scalable APIs
- Mentor junior engineers

Required Skills:
Python, FastAPI, PostgreSQL

Preferred Skills:
Docker, Kubernetes

Must have 5+ years of experience.
"""


def test_analyze_job_description_extracts_sections():
    analysis = analyze_job_description(JOB_TEXT)

    assert "Python" in analysis.required_skills
    assert "PostgreSQL" in analysis.required_skills
    assert "Docker" in analysis.preferred_skills
    assert analysis.min_experience_years == 5
    assert len(analysis.responsibilities) == 2
