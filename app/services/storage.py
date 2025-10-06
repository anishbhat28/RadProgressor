from sqlalchemy import create_engine, Column, String, Float, DateTime, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.sqlite import JSON
from datetime import datetime
from typing import List, Dict, Any, Optional
import json

from app.config import DATABASE_URL

Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"
    patient_id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Study(Base):
    __tablename__ = "studies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String, nullable=False)
    study_date = Column(String, nullable=False)
    cv_result = Column(JSON)
    nlp_result = Column(JSON)
    progression_score = Column(Float)
    genai_result = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def upsert_patient(patient_id: str) -> None:
    db = SessionLocal()
    try:
        patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
        if not patient:
            patient = Patient(patient_id=patient_id)
            db.add(patient)
            db.commit()
    finally:
        db.close()

def add_study(patient_id: str, study_date: str, cv_result: Dict, nlp_result: Dict, 
              progression_score: float, genai_result: Dict) -> None:
    db = SessionLocal()
    try:
        study = Study(
            patient_id=patient_id,
            study_date=study_date,
            cv_result=cv_result,
            nlp_result=nlp_result,
            progression_score=progression_score,
            genai_result=genai_result
        )
        db.add(study)
        db.commit()
    finally:
        db.close()

def get_timeline(patient_id: str) -> List[Dict[str, Any]]:
    db = SessionLocal()
    try:
        studies = db.query(Study).filter(Study.patient_id == patient_id).order_by(Study.study_date).all()
        timeline = []
        for study in studies:
            timeline.append({
                "date": study.study_date,
                "progression_score": study.progression_score,
                "key_labels": study.cv_result.get("labels", {}),
                "change": study.nlp_result.get("change", "stable")
            })
        return timeline
    finally:
        db.close()

def get_last_study(patient_id: str) -> Optional[Dict[str, Any]]:
    db = SessionLocal()
    try:
        study = db.query(Study).filter(Study.patient_id == patient_id).order_by(Study.study_date.desc()).first()
        if study:
            return {
                "patient_id": study.patient_id,
                "study_date": study.study_date,
                "cv_result": study.cv_result,
                "nlp_result": study.nlp_result,
                "progression_score": study.progression_score,
                "genai_result": study.genai_result
            }
        return None
    finally:
        db.close()
