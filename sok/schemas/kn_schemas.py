# backend0/schemas/kn_schemas.py
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class KBClauseSubParBase(BaseModel):
    par_ident: str
    unify_cl: Optional[str] = None
    unify_par: Optional[str] = None
    cut: Optional[bool] = False
    value: Optional[str] = None

class KBClauseSubParCreate(KBClauseSubParBase):
    pass

class KBClauseSubPar(KBClauseSubParBase):
    id: int
    clause_sub_id: int
    model_config = ConfigDict(from_attributes=True)

class KBClauseSubBase(BaseModel):
    sub_id: int
    order: int

class KBClauseSubCreate(KBClauseSubBase):
    parameters: List[KBClauseSubParCreate] = []

class KBClauseSub(KBClauseSubBase):
    id: int
    clause_id: int
    parameters: List[KBClauseSubPar] = []
    model_config = ConfigDict(from_attributes=True)

class KBClauseParBase(BaseModel):
    par_ident: str
    par_description: Optional[str] = None

class KBClauseParCreate(KBClauseParBase):
    pass

class KBClausePar(KBClauseParBase):
    id: int
    clause_id: int
    model_config = ConfigDict(from_attributes=True)

class KBClauseBase(BaseModel):
    cl_ident: str
    cl_description: Optional[str] = None
    cl_category: str = 'definicja'
    cl_view_name: Optional[str] = None
    cl_net: Optional[str] = None

class KBClauseCreate(KBClauseBase):
    parameters: List[KBClauseParCreate] = []
    subs: List[KBClauseSubCreate] = []

class KBClauseUpdate(KBClauseCreate):
    pass

class KBClause(KBClauseBase):
    id: int
    parameters: List[KBClausePar] = []
    subs: List[KBClauseSub] = []
    model_config = ConfigDict(from_attributes=True)

class KBClauseSimple(BaseModel):
    id: int
    cl_ident: str
    cl_description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class KBClauseListItem(KBClauseBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class KBClauseListResponse(BaseModel):
    total_count: int
    items: List[KBClauseListItem]

class Wynik(BaseModel):
    kod: int
    opis: str

class External(BaseModel):
    id: int
    ident : str
    api: Optional[str] = ''
    description: Optional[str] = ''
    provider: Optional[str] = ''
    url: Optional[str] = ''
    url_def: Optional[str] = ''
    cron: Optional[str] = ''
    gus_par: Optional[str] = ''
    days: Optional[int] = 0
    model_config = ConfigDict(from_attributes=True)

class ExternalPar(BaseModel):
    id : int
    external_id : int
    par_ident : str
    par_description : str

class ExternalDef(External):
    pars : List[ExternalPar] = []

class ExternalList(BaseModel):
    klucz: Optional[str] = None
    strona: int
    interfejsy: List[External] = []

class ViewListSchema(BaseModel):
    view_name: str
    model_config = ConfigDict(from_attributes=True)

class ColumnSchema(BaseModel):
    column_name: str
    data_type: str
    model_config = ConfigDict(from_attributes=True)
