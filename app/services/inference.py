from typing import Dict, Any, Tuple
from PIL import Image
from app.models.cv_model import predict
from app.models.nlp_model import extract_sections, classify_change
from app.models.progression import score, trend_summary
from app.models.genai import summarize_clinician, summarize_patient
from app.services.storage import upsert_patient, add_study, get_timeline

def analyze_study(patient_id: str, study_date: str, image: Image.Image, 
                 report_text: str = "") -> Dict[str, Any]:
    
    upsert_patient(patient_id)
    
    labels, severity_score = predict(image)
    
    sections = extract_sections(report_text) if report_text else {"findings": "", "impression": ""}
    change, delta = classify_change(report_text) if report_text else ("stable", 0)
    
    progression_score = score(severity_score, delta)
    
    timeline = get_timeline(patient_id)
    trend = trend_summary([(entry["date"], entry["progression_score"]) for entry in timeline])
    
    genai_clinician = summarize_clinician(sections.get("findings", ""), labels, trend)
    genai_patient = summarize_patient(sections.get("findings", ""), labels, trend)
    
    cv_result = {"labels": labels, "severity_score": severity_score}
    nlp_result = {"sections": sections, "change": change, "delta": delta}
    progression_result = {
        "progression_score": progression_score,
        "trend_direction": trend["direction"],
        "last_delta": trend["last_delta"]
    }
    genai_result = {
        "clinician_summary": genai_clinician,
        "patient_summary": genai_patient
    }
    
    add_study(patient_id, study_date, cv_result, nlp_result, progression_score, genai_result)
    
    return {
        "patient_id": patient_id,
        "study_date": study_date,
        "cv_result": cv_result,
        "nlp_result": nlp_result,
        "progression_result": progression_result,
        "genai_result": genai_result
    }
