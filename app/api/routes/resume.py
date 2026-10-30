from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.config import settings
from app.schemas.resume import ParsedResume
from app.services.resume_parser import parse_resume

router = APIRouter(prefix="/resume", tags=["Resume"])

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


@router.post("/upload", response_model=ParsedResume)
async def upload_resume(file: UploadFile = File(...)):
    filename = file.filename or ""
    extension = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(status_code=413, detail=f"File exceeds the {settings.MAX_UPLOAD_SIZE_MB}MB limit")

    try:
        return parse_resume(content, extension)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
