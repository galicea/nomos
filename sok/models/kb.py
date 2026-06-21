# backend0/models/kb.py
from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db.base import Base

class KBClause(Base):
  __tablename__ = 'kb_clause'
  id = Column(Integer, primary_key=True)
  cl_ident = Column(String(100), unique=True, index=True)
  cl_description = Column(Text)
  cl_category = Column(Enum('definicja', 'baza', name='clcategory'), default='definicja')
  cl_view_name = Column(String(100))
  cl_net = Column(String(100))

  subs = relationship("KBClauseSub", back_populates="clause", cascade="all, delete-orphan", passive_deletes=True)
  parameters = relationship("KBClausePar", back_populates="clause", cascade="all, delete-orphan", passive_deletes=True)

class KBClausePar(Base):
  __tablename__ = 'kb_clause_par'
  id = Column(Integer, primary_key=True)
  clause_id = Column(Integer, ForeignKey('kb_clause.id', ondelete="CASCADE"))
  par_ident = Column(String(100))
  par_description = Column(Text)
  clause = relationship("KBClause", back_populates="parameters")

class KBClauseSub(Base):
  __tablename__ = 'kb_clause_sub'
  id = Column(Integer, primary_key=True)
  clause_id = Column(Integer, ForeignKey('kb_clause.id', ondelete="CASCADE"))
  sub_id = Column(Integer)
  order = Column(Integer)
  clause = relationship("KBClause", back_populates="subs")
  parameters = relationship("KBClauseSubPar", back_populates="sub_clause", cascade="all, delete-orphan", passive_deletes=True)

class KBClauseSubPar(Base):
  __tablename__ = 'kb_clause_sub_par'
  id = Column(Integer, primary_key=True)
  clause_sub_id = Column(Integer, ForeignKey('kb_clause_sub.id', ondelete="CASCADE"))
  par_ident = Column(String(100))
  unify_cl = Column(String(100))
  unify_par = Column(String(100))
  active = Column(Boolean, default=True)
  cut = Column(Boolean, default=False)
  value = Column(String(255))
  sub_clause = relationship("KBClauseSub", back_populates="parameters")

class KBExternal(Base):
    __tablename__ = 'kb_external'
    id = Column(Integer, primary_key=True)
    ident = Column(String(100))
    api = Column(String(256))
    description = Column(Text)
    provider = Column(String(45))
    url = Column(String(256))
    url_def = Column(String(256))
    cron = Column(String(256))
    gus_par = Column(String(10))
    days = Column(Integer, default=7)

class KBExternalPar(Base):
    __tablename__ = 'kb_external_par'
    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(Integer)
    par_ident = Column(String(100))
    par_description = Column(Text)
