import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
API_PORT: int = int(os.getenv("API_PORT", "8000"))

DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./radprogressor.db")

CV_MODEL_NAME: str = os.getenv("CV_MODEL_NAME", "densenet121")
NLP_MODEL_NAME: str = os.getenv("NLP_MODEL_NAME", "emilyalsentzer/Bio_ClinicalBERT")

OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")

DEFAULT_ALPHA: float = 0.7
DEFAULT_BETA: float = 0.3

CHEST_XRAY_LABELS = [
    "atelectasis",
    "consolidation", 
    "effusion",
    "infiltration",
    "pneumonia"
]
