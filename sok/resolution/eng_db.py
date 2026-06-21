# backend0/resolution/eng_db.py
import csv
from sqlalchemy.orm import Session, joinedload
import models.kb as models
import schemas.kn_schemas as schemas
from .clause_engine import KnowledgeEngine

def load_cl(db: Session, engine: KnowledgeEngine, clause_id: int):
    clause: models.KBClause = db.query(models.KBClause).filter(
        models.KBClause.id == clause_id
    ).options(
        joinedload(models.KBClause.parameters),
        joinedload(models.KBClause.subs).subqueryload(models.KBClauseSub.parameters)
    ).first()

    if not clause:
        return

    if clause.subs:
        for sub in clause.subs:
            load_cl(db, engine, sub.sub_id)

    kbclause = schemas.KBClause.model_validate(clause)
    engine.load_clauses([kbclause])

def exec_to_csv(output, db : Session, clause_id: int, **input_params):
    engine = KnowledgeEngine()
    try:
        fieldnames = []
        load_cl(db, engine, clause_id)
        writer=None
        for res in engine.run(clause_id=clause_id, **input_params):
            if not fieldnames:
                for k in res.keys():
                    fieldnames.append(k)
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
            if writer:
              writer.writerow(res)
    finally:
        engine.close()
        db.close()
