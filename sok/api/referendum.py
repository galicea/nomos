from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from api.dependencies import get_db
import models.referendum as models
import schemas.referendum_schemas as schemas
from services.referendum_service import ReferendumService

router = APIRouter(
    prefix="/referendum",
    tags=["Referendum System"]
)

@router.post("", response_model=schemas.ReferendumResponse, status_code=status.HTTP_201_CREATED)
def create_referendum(ref_in: schemas.ReferendumCreate, db: Session = Depends(get_db)):
    db_ref = models.Referendum(
        case_id=ref_in.case_id,
        value_a=ref_in.value_a,
        value_b=ref_in.value_b,
        votes_a=0,
        votes_b=0,
        status="active"
    )
    db.add(db_ref)
    db.commit()
    db.refresh(db_ref)
    return db_ref

@router.get("/{ref_id}", response_model=schemas.ReferendumResponse)
def get_referendum(ref_id: int, db: Session = Depends(get_db)):
    ref = db.query(models.Referendum).filter(models.Referendum.id == ref_id).first()
    if not ref:
        raise HTTPException(status_code=404, detail="Referendum nie zostało odnalezione")
    return ref

@router.post("/{ref_id}/vote", response_model=schemas.ReferendumResponse)
def cast_vote(ref_id: int, vote_in: schemas.VoteInput, db: Session = Depends(get_db)):
    ref = db.query(models.Referendum).filter(models.Referendum.id == ref_id).first()
    if not ref:
        raise HTTPException(status_code=404, detail="Referendum nie zostało odnalezione")
    
    try:
        updated_ref = ReferendumService.cast_vote(ref, vote_in.option)
        db.commit()
        db.refresh(updated_ref)
        return updated_ref
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{ref_id}/close", response_model=schemas.ReferendumResponse)
def close_referendum(ref_id: int, db: Session = Depends(get_db)):
    ref = db.query(models.Referendum).filter(models.Referendum.id == ref_id).first()
    if not ref:
        raise HTTPException(status_code=404, detail="Referendum nie zostało odnalezione")

    updated_ref = ReferendumService.close_referendum(ref)
    db.commit()
    db.refresh(updated_ref)
    return updated_ref
