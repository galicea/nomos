# backend0/api/kn.py
import csv
from io import StringIO
from fastapi import Query, HTTPException, Depends, APIRouter, Response
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from starlette import status
from starlette.responses import StreamingResponse

from .dependencies import get_data_manager, get_db
import models.kb as models
from resolution.clause_engine import KnowledgeEngine
from resolution.eng_db import load_cl, exec_to_csv
import schemas.kn_schemas as schemas
from schemas.kn_schemas import ViewListSchema, ColumnSchema
from services.dbviews import ViewRepository
from services.knservice import DataManager

router = APIRouter(
  prefix="/kb",
  tags=['Knowledge Base'],
)

@router.get("/list", response_model=List[schemas.KBClauseSimple])
def get_clause_list(db: Session = Depends(get_db)):
  return db.query(models.KBClause).all()

@router.get("/{clause_id}", response_model=schemas.KBClause)
def get_clause(clause_id: int, db: Session = Depends(get_db)):
  clause = db.query(models.KBClause).filter(models.KBClause.id == clause_id).options(
    joinedload(models.KBClause.parameters),
    joinedload(models.KBClause.subs).subqueryload(models.KBClauseSub.parameters)
  ).first()
  if not clause:
    raise HTTPException(status_code=404, detail="Clause not found")
  return clause

@router.post("", response_model=schemas.KBClause, status_code=status.HTTP_201_CREATED)
def create_clause(clause_data: schemas.KBClauseCreate, db: Session = Depends(get_db)):
  existing = db.query(models.KBClause).filter(models.KBClause.cl_ident == clause_data.cl_ident).first()
  if existing:
    raise HTTPException(status_code=400, detail="cl_ident already exists")
  db_clause = models.KBClause(
    cl_ident=clause_data.cl_ident,
    cl_description=clause_data.cl_description,
    cl_category=clause_data.cl_category,
    cl_view_name=clause_data.cl_view_name,
    cl_net=clause_data.cl_net
  )
  for par_in in clause_data.parameters:
    db_par = models.KBClausePar(**par_in.model_dump(), clause=db_clause)
    db.add(db_par)
  for sub_in in clause_data.subs:
    db_sub = models.KBClauseSub(sub_id=sub_in.sub_id, order=sub_in.order, clause=db_clause)
    db.add(db_sub)
    for subpar_in in sub_in.parameters:
      db_subpar = models.KBClauseSubPar(**subpar_in.model_dump(), sub_clause=db_sub)
      db.add(db_subpar)
  try:
    db.add(db_clause)
    db.commit()
    db.refresh(db_clause)
    return get_clause(db_clause.id, db)
  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/{clause_id}", response_model=schemas.KBClause)
def update_clause(clause_id: int, clause_data: schemas.KBClauseUpdate, db: Session = Depends(get_db)):
  db_clause = db.query(models.KBClause).filter(models.KBClause.id == clause_id).first()
  if not db_clause:
    raise HTTPException(status_code=404, detail="Clause not found")
  if db_clause.cl_ident != clause_data.cl_ident:
    existing = db.query(models.KBClause).filter(models.KBClause.cl_ident == clause_data.cl_ident).first()
    if existing:
      raise HTTPException(status_code=400, detail="cl_ident already exists")
  db_clause.cl_ident = clause_data.cl_ident
  db_clause.cl_description = clause_data.cl_description
  db_clause.cl_category = clause_data.cl_category
  db_clause.cl_view_name = clause_data.cl_view_name
  db_clause.cl_net = clause_data.cl_net
  db_clause.parameters.clear()
  db_clause.subs.clear()
  db.flush()
  for par_in in clause_data.parameters:
    db_par = models.KBClausePar(**par_in.model_dump(), clause_id=db_clause.id)
    db.add(db_par)
  for sub_in in clause_data.subs:
    db_sub = models.KBClauseSub(sub_id=sub_in.sub_id, order=sub_in.order, clause_id=db_clause.id)
    db.add(db_sub)
    db.flush()
    for subpar_in in sub_in.parameters:
      db_subpar = models.KBClauseSubPar(**subpar_in.model_dump(), clause_sub_id=db_sub.id)
      db.add(db_subpar)
  try:
    db.commit()
    return get_clause(db_clause.id, db)
  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.delete("/{clause_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_clause(clause_id: int, db: Session = Depends(get_db)):
  db_clause = db.query(models.KBClause).filter(models.KBClause.id == clause_id).first()
  if not db_clause:
    raise HTTPException(status_code=404, detail="Clause not found")
  db.delete(db_clause)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("", response_model=schemas.KBClauseListResponse)
def list_clauses(skip: int = 0, limit: int = 25, db: Session = Depends(get_db)):
  query = db.query(models.KBClause)
  total_count = query.count()
  items = query.order_by(models.KBClause.cl_ident).offset(skip).limit(limit).all()
  return {"total_count": total_count, "items": items}

@router.get("/query/{clause_id}")
def exec_clause(clause_id: int, db: Session = Depends(get_db)):
  engine = KnowledgeEngine()
  try:
    load_cl(db, engine, clause_id)
    results = list(engine.run(clause_id=clause_id))
    if results:
      output = StringIO()
      writer = csv.writer(output)
      for res in results:
        writer.writerow(res.values())
      output.seek(0)
      return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=result.csv"}
      )
    else:
      return {"message": "Brak wyników"}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  finally:
    engine.close()


@router.get("/views/list", response_model=List[schemas.ViewListSchema])
def list_views(db: Session = Depends(get_db)):
  repo = ViewRepository(db)
  return repo.get_view_list()


@router.get("/views/{view_name}/structure", response_model=List[schemas.ColumnSchema])
def view_structure(view_name: str, db: Session = Depends(get_db)):
  repo = ViewRepository(db)
  return repo.get_view_structure(view_name)


@router.get("/external", response_model=schemas.ExternalList)
def get_external_list(key: Optional[str] = None, page: int = 1, limit: int = 10, dm: DataManager = Depends(get_data_manager)):
  sources = dm.KBSources(key=key or '', page=page, limit=limit)
  return {
    "klucz": key,
    "strona": page,
    "interfejsy": sources
  }


@router.post("/external", response_model=schemas.External, status_code=status.HTTP_201_CREATED)
def create_external_source(source_in: schemas.External, dm: DataManager = Depends(get_data_manager)):
  db_source = models.KBExternal(
    ident=source_in.ident,
    api=source_in.api,
    description=source_in.description,
    provider=source_in.provider,
    url=source_in.url,
    url_def=source_in.url_def,
    cron=source_in.cron,
    gus_par=source_in.gus_par,
    days=source_in.days
  )
  dm.AddExternal(db_source)
  return db_source


@router.put("/external/{source_id}", response_model=schemas.External)
def update_external_source(source_id: int, source_in: schemas.External, dm: DataManager = Depends(get_data_manager)):
  db_source = models.KBExternal(
    id=source_id,
    ident=source_in.ident,
    api=source_in.api,
    description=source_in.description,
    provider=source_in.provider,
    url=source_in.url,
    url_def=source_in.url_def,
    cron=source_in.cron,
    gus_par=source_in.gus_par,
    days=source_in.days
  )
  updated = dm.UpdateExternal(db_source)
  if not updated:
    raise HTTPException(status_code=404, detail="External source not found")
  return updated


@router.get("/external/{source_id}", response_model=schemas.External)
def get_external_source(source_id: int, dm: DataManager = Depends(get_data_manager)):
  source = dm.get_KBSource(source_id)
  if not source:
    raise HTTPException(status_code=404, detail="External source not found")
  return source


