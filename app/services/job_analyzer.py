"""Heuristic job description analysis.

Rule-based section/skill extraction keeps results traceable to the
source text, which the matching step relies on to avoid fabricating gaps.
"""
import re
from typing import List

from app.schemas.job_description import JobDescriptionAnalysis

EXPERIENCE_RE = re.compile(r"(\d+)\+?\s*(?:years|yrs)", re.IGNORECASE)

SECTION_HEADERS = {
    "required_skills": ["required skills", "requirements", "must have", "qualifications"],
    "preferred_skills": ["preferred skills", "nice to have", "preferred qualifications", "bonus"],
    "responsibilities": ["responsibilities", "what you'll do", "duties", "role overview"],
}


def _detect_section(line: str):
    cleaned = line.strip().lower().rstrip(":")
    for section, keywords in SECTION_HEADERS.items():
        if any(cleaned.startswith(keyword) for keyword in keywords):
            return section
    return None


def _split_sections(text: str) -> dict:
    sections: dict = {name: [] for name in SECTION_HEADERS}
    current = None
    for line in text.splitlines():
        if not line.strip():
            continue
        detected = _detect_section(line)
        if detected:
            current = detected
            continue
        if current:
            sections[current].append(line.strip().lstrip("-•* ").strip())
    return sections


def _split_items(lines: List[str]) -> List[str]:
    items: List[str] = []
    for line in lines:
        parts = re.split(r"[,;]", line) if "," in line or ";" in line else [line]
        items.extend(p.strip() for p in parts if p.strip())
    return items


def analyze_job_description(text: str) -> JobDescriptionAnalysis:
    if not text.strip():
        raise ValueError("Job description text is empty")

    sections = _split_sections(text)
    experience_match = EXPERIENCE_RE.search(text)

    return JobDescriptionAnalysis(
        required_skills=_split_items(sections["required_skills"]),
        preferred_skills=_split_items(sections["preferred_skills"]),
        responsibilities=sections["responsibilities"],
        min_experience_years=int(experience_match.group(1)) if experience_match else None,
        raw_text=text,
    )
