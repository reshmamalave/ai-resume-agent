from pydantic import BaseModel

from app.schemas.resume import ParsedResume


class GenerateRequest(BaseModel):
    resume: ParsedResume
    # File is only produced once a human has reviewed and approved the content.
    approved: bool = False
    file_format: str = "docx"
