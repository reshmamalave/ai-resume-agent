from docx import Document

from app.schemas.resume import ContactInfo, ParsedResume
from app.services.resume_generator import generate_docx


def test_generate_docx_contains_expected_sections():
    resume = ParsedResume(
        contact=ContactInfo(name="Jane Doe", email="jane@example.com"),
        summary="Experienced backend engineer.",
        skills=["Python", "FastAPI"],
        raw_text="...",
    )

    file_bytes = generate_docx(resume)

    import io

    parsed = Document(io.BytesIO(file_bytes))
    text = "\n".join(p.text for p in parsed.paragraphs)

    assert "Jane Doe" in text
    assert "jane@example.com" in text
    assert "Python, FastAPI" in text
