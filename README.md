# RadProgressor - Radiology Progression Lite

Upload serial chest X-rays + reports → get per-scan findings, a time-series "progression score," and a patient-friendly GenAI summary.

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

- **Computer Vision**: Multi-label chest X-ray analysis (atelectasis, consolidation, effusion, infiltration, pneumonia)
- **NLP**: Radiology report parsing and change detection (improved/stable/worsened)
- **Progression Tracking**: Time-series progression scoring with trend analysis
- **GenAI Summaries**: Clinical and patient-friendly explanations with safety guardrails

## API Endpoints

- `POST /api/analyze` - Analyze a chest X-ray study
- `GET /api/patient/{patient_id}/timeline` - Get patient progression timeline
- `GET /api/patient/{patient_id}/snapshot` - Get latest study with summaries

## Tech Stack

- **Backend**: FastAPI + SQLAlchemy + SQLite
- **ML**: PyTorch + torchvision + HuggingFace Transformers
- **Frontend**: Streamlit
- **GenAI**: OpenAI (optional)

## Disclaimer

This tool is for research and educational purposes only. It does not provide medical advice, diagnosis, or treatment recommendations.
