from typing import List, Optional

from pydantic import BaseModel


class ContactInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None


class Experience(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    dates: Optional[str] = None
    details: List[str] = []


class Education(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    dates: Optional[str] = None


class ParsedResume(BaseModel):
    contact: ContactInfo = ContactInfo()
    summary: Optional[str] = None
    skills: List[str] = []
    experience: List[Experience] = []
    education: List[Education] = []
    raw_text: str
