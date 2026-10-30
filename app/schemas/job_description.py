from typing import List, Optional

from pydantic import BaseModel


class JobDescriptionRequest(BaseModel):
    text: str


class JobDescriptionAnalysis(BaseModel):
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    responsibilities: List[str] = []
    min_experience_years: Optional[int] = None
    raw_text: str
