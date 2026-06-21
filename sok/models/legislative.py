# backend0/models/legislative.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base

class LawProject(Base):
    __tablename__ = 'law_project'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    text = Column(Text, nullable=False)
    formal_proof = Column(Text, nullable=True)
    status = Column(String(50), default='draft')  # draft, pending, verified, rejected_logic, rejected_value
    created_at = Column(DateTime, default=datetime.utcnow)

    reports = relationship("VerificationReport", back_populates="law_project", cascade="all, delete-orphan")

class VerificationReport(Base):
    __tablename__ = 'verification_report'
    id = Column(Integer, primary_key=True, index=True)
    law_project_id = Column(Integer, ForeignKey('law_project.id', ondelete="CASCADE"))
    result = Column(String(50), nullable=False)  # ZGODNY, NIEZGODNY_LOGIKA, NIEZGODNY_WARTOSC
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    law_project = relationship("LawProject", back_populates="reports")
