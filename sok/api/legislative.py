# backend0/api/legislative.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from typing import List

from api.dependencies import get_db
import models.legislative as models
import schemas.legislative_schemas as schemas
from services.legislative_service import LegislativeService

router = APIRouter(
    prefix="/legislative",
    tags=["Legislative System"]
)

@router.post("/bills", response_model=schemas.LawProject, status_code=status.HTTP_201_CREATED)
def create_bill(bill_in: schemas.LawProjectCreate, db: Session = Depends(get_db)):
    # Walidacja formalna struktury przepisu (UC01)
    is_valid, msg = LegislativeService.validate_draft_structure(bill_in.text, bill_in.formal_proof or "")
    
    db_bill = models.LawProject(
        title=bill_in.title,
        text=bill_in.text,
        formal_proof=bill_in.formal_proof,
        status='pending' if is_valid else 'draft'
    )
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)

    # Zapisujemy automatycznie raport ze wstępnej weryfikacji struktury
    db_report = models.VerificationReport(
        law_project_id=db_bill.id,
        result='ZGODNY' if is_valid else 'NIEZGODNY_LOGIKA',
        details=msg
    )
    db.add(db_report)
    db.commit()
    
    return db_bill

@router.get("/bills/{bill_id}", response_model=schemas.LawProject)
def get_bill(bill_id: int, db: Session = Depends(get_db)):
    bill = db.query(models.LawProject).filter(models.LawProject.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Projekt ustawy nie został znaleziony")
    return bill

@router.post("/bills/{bill_id}/verify", response_model=schemas.VerificationReportResponse)
def verify_bill(bill_id: int, db: Session = Depends(get_db)):
    # Pobieramy projekt
    bill = db.query(models.LawProject).filter(models.LawProject.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Projekt ustawy nie został znaleziony")

    # UC02: Weryfikacja spójności i hierarchii wartości
    result, details = LegislativeService.verify_consistency_and_hierarchy(bill.text, bill.formal_proof or "")
    
    bill.status = 'verified' if result == 'ZGODNY' else ('rejected_logic' if result == 'NIEZGODNY_LOGIKA' else 'rejected_value')
    
    db_report = models.VerificationReport(
        law_project_id=bill.id,
        result=result,
        details=details
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    
    return db_report

@router.get("/bills/{bill_id}/report", response_model=List[schemas.VerificationReportResponse])
def get_bill_reports(bill_id: int, db: Session = Depends(get_db)):
    reports = db.query(models.VerificationReport).filter(models.VerificationReport.law_project_id == bill_id).order_by(models.VerificationReport.id.desc()).all()
    return reports
