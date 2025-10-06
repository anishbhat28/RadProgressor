import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.storage import upsert_patient, add_study
from datetime import datetime, timedelta

def seed_demo_data():
    patient_id = "DEMO001"
    upsert_patient(patient_id)
    
    base_date = datetime.now() - timedelta(days=30)
    
    studies = [
        {
            "date": (base_date + timedelta(days=0)).strftime("%Y-%m-%d"),
            "cv_result": {
                "labels": {
                    "atelectasis": 0.15,
                    "consolidation": 0.08,
                    "effusion": 0.12,
                    "infiltration": 0.22,
                    "pneumonia": 0.05
                },
                "severity_score": 0.22
            },
            "nlp_result": {
                "sections": {
                    "findings": "Mild bilateral lower lobe atelectasis. No acute consolidation.",
                    "impression": "Stable chest X-ray with mild atelectasis."
                },
                "change": "stable",
                "delta": 0
            },
            "progression_score": 0.35,
            "genai_result": {
                "clinician_summary": "Baseline study shows mild atelectasis. No acute findings. Recommend clinical correlation.",
                "patient_summary": "Your chest X-ray shows some minor changes that are common and not concerning. Please discuss with your doctor."
            }
        },
        {
            "date": (base_date + timedelta(days=14)).strftime("%Y-%m-%d"),
            "cv_result": {
                "labels": {
                    "atelectasis": 0.28,
                    "consolidation": 0.15,
                    "effusion": 0.18,
                    "infiltration": 0.35,
                    "pneumonia": 0.12
                },
                "severity_score": 0.35
            },
            "nlp_result": {
                "sections": {
                    "findings": "Increased bilateral lower lobe opacities. New small pleural effusion.",
                    "impression": "Progression of findings compared to prior study."
                },
                "change": "worsened",
                "delta": 1
            },
            "progression_score": 0.58,
            "genai_result": {
                "clinician_summary": "Progression noted with increased opacities and new effusion. Consider clinical correlation and possible treatment adjustment.",
                "patient_summary": "Your recent chest X-ray shows some changes compared to before. Your doctor will discuss what this means for your care."
            }
        },
        {
            "date": (base_date + timedelta(days=28)).strftime("%Y-%m-%d"),
            "cv_result": {
                "labels": {
                    "atelectasis": 0.18,
                    "consolidation": 0.08,
                    "effusion": 0.12,
                    "infiltration": 0.25,
                    "pneumonia": 0.06
                },
                "severity_score": 0.25
            },
            "nlp_result": {
                "sections": {
                    "findings": "Improvement in bilateral lower lobe opacities. Decreased pleural effusion.",
                    "impression": "Improvement compared to prior study."
                },
                "change": "improved",
                "delta": -1
            },
            "progression_score": 0.42,
            "genai_result": {
                "clinician_summary": "Improvement noted with decreased opacities and effusion. Continue current management.",
                "patient_summary": "Good news! Your recent chest X-ray shows improvement compared to the previous one. Keep following your treatment plan."
            }
        }
    ]
    
    for study in studies:
        add_study(
            patient_id=patient_id,
            study_date=study["date"],
            cv_result=study["cv_result"],
            nlp_result=study["nlp_result"],
            progression_score=study["progression_score"],
            genai_result=study["genai_result"]
        )
    
    print(f"Seeded demo data for patient {patient_id} with {len(studies)} studies")

if __name__ == "__main__":
    seed_demo_data()
