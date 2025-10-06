from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import json

from app.schemas.io import AnalyzeRequest, StudyAnalysis, PatientTimeline, PatientSnapshot
from app.services.parsing import load_image
from app.services.inference import analyze_study
from app.services.storage import get_timeline, get_last_study
from app.models.progression import trend_summary

app = FastAPI(title="RadProgressor API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    pass

@app.get("/api/health")
async def health_check():
    return {"ok": True}

@app.post("/api/analyze")
async def analyze(
    patient_id: str = Form(...),
    study_date: str = Form(...),
    image: UploadFile = File(...),
    report: Optional[str] = Form(None)
):
    try:
        image_content = await image.read()
        pil_image, _ = load_image(image_content, image.filename)
        
        result = analyze_study(patient_id, study_date, pil_image, report or "")
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/patient/{patient_id}/timeline")
async def get_patient_timeline(patient_id: str):
    try:
        timeline = get_timeline(patient_id)
        return {"patient_id": patient_id, "timeline": timeline}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/patient/{patient_id}/snapshot")
async def get_patient_snapshot(patient_id: str):
    try:
        last_study = get_last_study(patient_id)
        if not last_study:
            raise HTTPException(status_code=404, detail="No studies found for patient")
        
        timeline = get_timeline(patient_id)
        trend = trend_summary([(entry["date"], entry["progression_score"]) for entry in timeline])
        
        return {
            "patient_id": patient_id,
            "last_study": last_study,
            "timeline_summary": trend
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
