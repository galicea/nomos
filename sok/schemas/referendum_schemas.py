# backend0/schemas/referendum_schemas.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ReferendumCreate(BaseModel):
    case_id: Optional[int] = None
    value_a: str
    value_b: str

class VoteInput(BaseModel):
    option: str  # 'A' or 'B'

class ReferendumResponse(BaseModel):
    id: int
    case_id: Optional[int] = None
    value_a: str
    value_b: str
    votes_a: int
    votes_b: int
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
