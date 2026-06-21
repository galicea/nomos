# backend0/models/lt.py
from sqlalchemy import Column, Integer, String, Text, Float
from db.base import Base

class SemanticNode(Base):
    __tablename__ = 'semantic_node'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    kind = Column(Integer)
    fuzzy = Column(Float, default=1.0)

class SemanticEdge(Base):
    __tablename__ = 'semantic_edge'
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer)
    target_id = Column(Integer)
    weight = Column(Float)

class Question(Base):
    __tablename__ = 'question'
    question_id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text)
    intent = Column(String(255))

class QuestionPredicateMapping(Base):
    __tablename__ = 'question_predicate_mapping'
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer)
    predicate_id = Column(String(255))

class Predicate(Base):
    __tablename__ = 'predicate'
    predicate_id = Column(String(255), primary_key=True, index=True)
    category = Column(String(255))
    logic_expression = Column(Text)
    short_answer = Column(Text)
