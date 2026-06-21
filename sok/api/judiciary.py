from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
import json

from api.dependencies import get_db
import models.judiciary as models
import schemas.judiciary_schemas as schemas
from services.judiciary_service import JudiciaryService

router = APIRouter(
    prefix="/judiciary",
    tags=["Judiciary System"]
)

@router.post("/cases", response_model=schemas.CourtCaseResponse, status_code=status.HTTP_201_CREATED)
def create_case(case_in: schemas.CourtCaseCreate, db: Session = Depends(get_db)):
    db_case = models.CourtCase(
        title=case_in.title,
        facts=case_in.facts,
        difficulty=case_in.difficulty,
        status="pending"
    )
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    return db_case

@router.get("/cases/{case_id}", response_model=schemas.CourtCaseResponse)
def get_case(case_id: int, db: Session = Depends(get_db)):
    case = db.query(models.CourtCase).filter(models.CourtCase.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Sprawa sądowa nie została odnaleziona")
    return case

@router.get("/cases/{case_id}/gaps")
def get_case_gaps(case_id: int, db: Session = Depends(get_db)):
    case = db.query(models.CourtCase).filter(models.CourtCase.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Sprawa sądowa nie została odnaleziona")
    
    gaps = JudiciaryService.get_decision_gaps(case.facts)
    case.decision_gaps = json.dumps(gaps)
    db.commit()
    return gaps

@router.post("/cases/{case_id}/adjudicate", response_model=schemas.CourtCaseResponse)
def adjudicate_case(case_id: int, db: Session = Depends(get_db), params_in: schemas.AdjudicateHardInput = None):
    case = db.query(models.CourtCase).filter(models.CourtCase.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Sprawa sądowa nie została odnaleziona")

    if case.difficulty == "easy":
        success, judgment, path = JudiciaryService.adjudicate_easy(case.facts)
        if not success:
            # If easy rules failed, switch to hard mode automatically
            case.difficulty = "hard"
            case.status = "pending"
            db.commit()
            raise HTTPException(
                status_code=400,
                detail="Brak jednoznacznego dopasowania reguł logicznych dla spraw łatwych. Sprawa przełączona na tryb trudny."
            )
        case.final_judgment = judgment
        case.logical_path = path
        case.status = "adjudicated"
        db.commit()
        db.refresh(case)
        return case

    else:  # hard case
        if not params_in or not params_in.parameters:
            raise HTTPException(
                status_code=400,
                detail="Dla spraw trudnych wymagane jest przesłanie parametrów oceny wagowej."
            )
        result = JudiciaryService.calculate_alexy_weight(params_in.parameters)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        case.final_judgment = result["final_judgment"]
        case.logical_path = result["logical_path"]
        case.status = result["status"]
        db.commit()
        db.refresh(case)
        return case

@router.post("/simulate", response_model=schemas.SimulationResult)
def simulate_case_effects(sim_in: schemas.SimulationInput):
    result = JudiciaryService.simulate_effects(sim_in.facts)
    return result
