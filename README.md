# AI Resume Agent

An AI-assisted agent that tailors resumes to specific job descriptions. It parses an
uploaded resume, analyzes a job description, matches the two, and produces an
ATS-friendly, human-approved revision — without ever inventing skills or experience
the candidate doesn't have.

## Design principle

> The agent must never invent experience or skills. If your resume lists MySQL but a
> job requires PostgreSQL, PostgreSQL is flagged as a gap — it is never silently added.

This is enforced in code: `resume_matcher.py` only ever reports missing skills as gaps,
and the LangGraph workflow's validate/revise nodes strip any skill the optimize step
didn't find in the original resume.

## Roadmap

| Step | Feature | Status |
|---|---|---|
| 1 | FastAPI foundation (project setup, config, health check, tests) | Done |
| 2 | Resume upload and parsing (PDF/DOCX → structured data) | Done |
| 3 | Job description analysis (skills, responsibilities, experience) | Done |
| 4 | Resume matching (matching/missing/extra skills, score) | Done |
| 5 | LangGraph agent workflow (analyze → match → optimize → validate → revise) | Done |
| 6 | Resume generation (ATS-friendly DOCX, human approval required) | Done |
| 7 | Production readiness (MySQL persistence, Docker, logging) | Planned |

## Project structure

```
app/
├── main.py                   # FastAPI app, router registration
├── api/routes/                # HTTP endpoints
│   ├── health.py
│   ├── resume.py               # POST /resume/upload
│   ├── job.py                   # POST /job/analyze
│   ├── match.py                  # POST /match/
│   ├── agent.py                   # POST /agent/run (LangGraph workflow)
│   └── generate.py                 # POST /resume/generate
├── agents/
│   ├── state.py                    # Shared LangGraph state
│   └── workflow.py                  # analyze -> match -> optimize -> validate -> revise
├── core/config.py                    # Settings (env-driven)
├── schemas/                            # Pydantic models
├── services/                            # Business logic (parsing, analysis, matching, generation)
└── db/                                    # Reserved for step 7 (MySQL persistence)
tests/                                       # pytest unit tests
```

## Prerequisites

- Python 3.11 or newer
- pip

### Windows note

If `python --version` or `py --version` fails with "the system cannot find the file
specified" even though `py -0p` lists an installed version, the Python install is
broken/incomplete. Reinstall Python from [python.org](https://www.python.org/downloads/)
(check **Add python.exe to PATH** during setup) rather than trying to repair the
existing install.

## Setup

1. **Clone and enter the project**

   ```powershell
   cd "ai-resume-agent"
   ```

2. **Create and activate a virtual environment**

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   On macOS/Linux:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   ```powershell
   Copy-Item .env.example .env
   ```

   Edit `.env` if needed. All values have working defaults — `OPENAI_API_KEY` is
   optional and only used for future LLM-assisted optimization.

## Running the app

```powershell
uvicorn app.main:app --reload
```

- App: http://127.0.0.1:8000/
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Running tests

```powershell
pytest
```

## API overview

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/resume/upload` | Upload a PDF/DOCX resume, get back structured data |
| POST | `/api/v1/job/analyze` | Analyze job description text |
| POST | `/api/v1/match/` | Compare a parsed resume against a job analysis |
| POST | `/api/v1/agent/run` | Run the full LangGraph workflow (analyze, match, optimize, validate, revise) |
| POST | `/api/v1/resume/generate` | Generate an ATS-friendly `.docx` (requires `approved: true`) |

A typical flow: upload a resume → paste a job description for analysis → run the agent
→ review the optimized resume and flagged skill gaps → approve → download the `.docx`.
