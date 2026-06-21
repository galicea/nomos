# backend0/models/referendum.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from db.base import Base

class Referendum(Base):
    __tablename__ = 'referendum'
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, nullable=True)  # Associated court case where deadlock occurred
    value_a = Column(String(100), nullable=False)  # e.g., 'Zasada Wolności'
    value_b = Column(String(100), nullable=False)  # e.g., 'Dobro Wspólnot'
    votes_a = Column(Integer, default=0)
    votes_b = Column(Integer, default=0)
    status = Column(String(50), default='active')  # active, completed_valid, completed_invalid
    created_at = Column(DateTime, default=datetime.utcnow)
