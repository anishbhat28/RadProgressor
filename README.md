# RadProgressor - Radiology Progression Lite

Serial chest X-rays + reports → get per-scan findings, a time-series "progression score," and a GenAI summary.

## Quick Start

### 1) Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp env.example .env
```

### 2) Seed Demo Data
```bash
python scripts/seed_demo.py
```

### 3) Run API
```bash
uvicorn app.main:app --reload
```

### 4) Run UI
```bash
streamlit run ui/app.py
```

## Features

- Multi-label chest X-ray analysis (atelectasis, consolidation, effusion, infiltration, pneumonia)
- Radiology report parsing and change detection (improved/stable/worsened)
- Time-series progression scoring with trend analysis
- Clinical and patient-friendly explanations with safety guardrails

## API Endpoints

- `POST /api/analyze` - Analyzes a chest X-ray study
- `GET /api/patient/{patient_id}/timeline` - Gets patient progression timeline
- `GET /api/patient/{patient_id}/snapshot` - Gets latest study with summaries

## Tech Stack

- **Backend**: FastAPI + SQLAlchemy + SQLite
- **ML**: PyTorch + torchvision + HuggingFace Transformers
- **Frontend**: Streamlit
- **GenAI**: OpenAI (optional)

## Disclaimer: Please DO NOT use this project for professional medical diagnoses. This is a personal project I created for learning and experience purposes ONLY. 
