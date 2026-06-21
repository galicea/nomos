# backend0/schemas/judiciary_schemas.py
from pydantic import BaseModel, ConfigDict
from typing import Dict, Any, Optional
from datetime import datetime

class CourtCaseCreate(BaseModel):
    title: str
    facts: str  # JSON-formatted facts string
    difficulty: Optional[str] = 'easy'

class CourtCaseResponse(BaseModel):
    id: int
    title: str
    facts: str
    difficulty: str
    status: str
    decision_gaps: Optional[str] = None
    final_judgment: Optional[str] = None
    logical_path: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class AdjudicateHardInput(BaseModel):
    # Mapping of parameter/weight identifiers to their assigned values (e.g. integer waga, float certainty)
    # Example: {"I_1": 4, "W_1": 4, "R_1": 1.0, "I_2": 1, "W_2": 4, "R_2": 0.5}
    parameters: Dict[str, Any]

class SimulationInput(BaseModel):
    facts: str
    proposed_law_id: Optional[int] = None

class SimulationResult(BaseModel):
    proposed_judgment: str
    logical_path: str
    impact_statement: str
