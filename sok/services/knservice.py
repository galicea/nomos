# backend0/services/knservice.py
from typing import List
from models.kb import KBClause, KBExternal

class DataManager():
  def __init__(self, db_session):
    self.db_session=db_session

  def KBSources(self, key='', page=1, limit=10):
    query = self.db_session.query(KBExternal)
    if key:
      query = query.filter(KBExternal.ident.like(f"%{key}%"))
    return query.order_by(KBExternal.id.desc()).offset((page-1)*limit).limit(limit).all()

  def AddExternal(self, data: KBExternal):
    self.db_session.add(data)
    self.db_session.commit()

  def UpdateExternal(self, data: KBExternal):
    obiekt = self.db_session.query(KBExternal).filter(KBExternal.id == data.id).first()
    if obiekt:
      for c in data.__table__.columns:
          if c.name != "id":
              setattr(obiekt, c.name, getattr(data, c.name))
      self.db_session.commit()
    return obiekt

  def get_KBSource(self, id):
    return self.db_session.query(KBExternal).filter(KBExternal.id == id).first()
