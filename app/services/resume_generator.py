"""ATS-friendly resume file generation (single column, no tables/images)."""
import io

from docx import Document
from docx.shared import Pt

from app.schemas.resume import ParsedResume


def generate_docx(resume: ParsedResume) -> bytes:
    document = Document()
    style = document.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)

    if resume.contact.name:
        document.add_heading(resume.contact.name, level=1)

    contact_line = " | ".join(
        value
        for value in [resume.contact.email, resume.contact.phone, resume.contact.linkedin, resume.contact.location]
        if value
    )
    if contact_line:
        document.add_paragraph(contact_line)

    if resume.summary:
        document.add_heading("Summary", level=2)
        document.add_paragraph(resume.summary)

    if resume.skills:
        document.add_heading("Skills", level=2)
        document.add_paragraph(", ".join(resume.skills))

    if resume.experience:
        document.add_heading("Experience", level=2)
        for exp in resume.experience:
            title_line = " - ".join(filter(None, [exp.title, exp.company, exp.dates]))
            document.add_paragraph(title_line)
            for detail in exp.details:
                document.add_paragraph(detail, style="List Bullet")

    if resume.education:
        document.add_heading("Education", level=2)
        for edu in resume.education:
            line = " - ".join(filter(None, [edu.degree, edu.institution, edu.dates]))
            document.add_paragraph(line)

    buffer = io.BytesIO()
    document.save(buffer)
    return buffer.getvalue()
