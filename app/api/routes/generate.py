import io

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.schemas.generation import GenerateRequest
from app.services.resume_generator import generate_docx

router = APIRouter(prefix="/resume", tags=["Resume"])

DOCX_MEDIA_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


@router.post("/generate")
async def generate_resume(payload: GenerateRequest):
    if not payload.approved:
        raise HTTPException(status_code=400, detail="Resume generation requires human approval (approved=true)")

    if payload.file_format != "docx":
        raise HTTPException(status_code=400, detail="Only 'docx' is currently supported")

    file_bytes = generate_docx(payload.resume)
    return StreamingResponse(
        io.BytesIO(file_bytes),
        media_type=DOCX_MEDIA_TYPE,
        headers={"Content-Disposition": "attachment; filename=resume.docx"},
    )
