# backend0/schemas/legislative_schemas.py
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class LawProjectCreate(BaseModel):
    title: str
    text: str
    formal_proof: Optional[str] = None

class VerificationReportResponse(BaseModel):
    id: int
    law_project_id: int
    result: str
    details: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class LawProject(BaseModel):
    id: int
    title: str
    text: str
    formal_proof: Optional[str] = None
    status: str
    created_at: datetime
    reports: List[VerificationReportResponse] = []
    model_config = ConfigDict(from_attributes=True)
