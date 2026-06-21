# backend0/models/judiciary.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from db.base import Base

class CourtCase(Base):
    __tablename__ = 'court_case'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    facts = Column(Text, nullable=False)  # JSON representation of case facts/predicates
    difficulty = Column(String(50), default='easy')  # easy, hard
    status = Column(String(50), default='pending')  # pending, adjudicated, deadlock
    decision_gaps = Column(Text, nullable=True)  # JSON describing parameters (weights, etc.) to be filled
    final_judgment = Column(Text, nullable=True)
    logical_path = Column(Text, nullable=True)  # Detailed trace of the logic applied
    created_at = Column(DateTime, default=datetime.utcnow)
