"""Heuristic resume parsing for PDF and DOCX uploads.

No LLM is used here: extraction is purely rule-based so the parsed output
only ever contains what was literally present in the source file.
"""
import io
import re
from typing import List

import pdfplumber
from docx import Document

from app.schemas.resume import ContactInfo, Education, Experience, ParsedResume

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"(\+?\d[\d\s().-]{7,}\d)")
LINKEDIN_RE = re.compile(r"(https?://)?(www\.)?linkedin\.com/\S+", re.IGNORECASE)

SECTION_HEADERS = {
    "summary": ["summary", "objective", "profile"],
    "skills": ["skills", "technical skills", "core competencies"],
    "experience": ["experience", "work experience", "employment history"],
    "education": ["education", "academic background"],
}


def extract_text_from_pdf(file_bytes: bytes) -> str:
    text_parts: List[str] = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts)


def extract_text_from_docx(file_bytes: bytes) -> str:
    document = Document(io.BytesIO(file_bytes))
    return "\n".join(p.text for p in document.paragraphs)


def _detect_section(line: str):
    cleaned = line.strip().lower().rstrip(":")
    for section, keywords in SECTION_HEADERS.items():
        if cleaned in keywords:
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
            sections[current].append(line.strip())
    return sections


def _parse_contact(text: str) -> ContactInfo:
    email_match = EMAIL_RE.search(text)
    phone_match = PHONE_RE.search(text)
    linkedin_match = LINKEDIN_RE.search(text)
    first_line = next((l.strip() for l in text.splitlines() if l.strip()), None)

    return ContactInfo(
        name=first_line,
        email=email_match.group(0) if email_match else None,
        phone=phone_match.group(0) if phone_match else None,
        linkedin=linkedin_match.group(0) if linkedin_match else None,
    )


def _parse_skills(lines: List[str]) -> List[str]:
    skills: List[str] = []
    for line in lines:
        parts = re.split(r"[,•|/]", line)
        skills.extend(p.strip() for p in parts if p.strip())
    # Preserve order while removing duplicates.
    seen = set()
    unique_skills = []
    for skill in skills:
        key = skill.lower()
        if key not in seen:
            seen.add(key)
            unique_skills.append(skill)
    return unique_skills


def _parse_experience(lines: List[str]) -> List[Experience]:
    entries: List[Experience] = []
    current: Experience = None
    for line in lines:
        if line.startswith(("-", "•", "*")):
            if current is not None:
                current.details.append(line.lstrip("-•* ").strip())
            continue
        if current is not None:
            entries.append(current)
        current = Experience(title=line.strip())
    if current is not None:
        entries.append(current)
    return entries


def _parse_education(lines: List[str]) -> List[Education]:
    return [Education(degree=line) for line in lines]


def parse_resume(file_bytes: bytes, extension: str) -> ParsedResume:
    if extension == ".pdf":
        text = extract_text_from_pdf(file_bytes)
    elif extension == ".docx":
        text = extract_text_from_docx(file_bytes)
    else:
        raise ValueError(f"Unsupported file extension: {extension}")

    if not text.strip():
        raise ValueError("No extractable text found in the uploaded file")

    sections = _split_sections(text)

    return ParsedResume(
        contact=_parse_contact(text),
        summary=" ".join(sections["summary"]) or None,
        skills=_parse_skills(sections["skills"]),
        experience=_parse_experience(sections["experience"]),
        education=_parse_education(sections["education"]),
        raw_text=text,
    )
