import pytest
import requests
import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"ok": True}

def test_analyze_endpoint():
    test_data = {
        "patient_id": "TEST001",
        "study_date": "2024-01-01",
        "report": "FINDINGS: No acute findings. IMPRESSION: Normal chest X-ray."
    }
    
    with open("data/samples/test_image.png", "rb") as f:
        files = {"image": ("test.png", f, "image/png")}
        response = client.post("/api/analyze", data=test_data, files=files)
    
    assert response.status_code == 200
    result = response.json()
    assert "cv_result" in result
    assert "nlp_result" in result
    assert "progression_result" in result
    assert "genai_result" in result

def test_timeline_endpoint():
    response = client.get("/api/patient/DEMO001/timeline")
    assert response.status_code == 200
    result = response.json()
    assert "patient_id" in result
    assert "timeline" in result

def test_snapshot_endpoint():
    response = client.get("/api/patient/DEMO001/snapshot")
    assert response.status_code == 200
    result = response.json()
    assert "patient_id" in result
    assert "last_study" in result
    assert "timeline_summary" in result
