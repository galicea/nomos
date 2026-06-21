# backend0/schemas/lt_schemas.py
from pydantic import BaseModel
from typing import List, Dict, Optional

class QuestionPost(BaseModel):
    message: str
    conversation_history: Optional[List[Dict[str, str]]] = None
