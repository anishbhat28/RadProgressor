import os
from typing import Dict, Any

SYSTEM = "You are a careful clinical writing assistant. Do not diagnose. Use hedging and uncertainty. Keep it concise."

def summarize_clinician(findings: str, labels: Dict[str, float], trend: Dict[str, Any]) -> str:
    if "OPENAI_API_KEY" not in os.environ:
        return ("Impression (draft): Pattern suggests possible changes in the above labels. "
                f"Recent trajectory is {trend['direction']} (Δ={trend['last_delta']}). "
                "Correlate clinically and compare with prior imaging.")
    return "LLM summary placeholder."

def summarize_patient(findings: str, labels: Dict[str, float], trend: Dict[str, Any]) -> str:
    if "OPENAI_API_KEY" not in os.environ:
        return ("Plain-language note: Your recent chest images show signs that may relate to the lungs. "
                f"Overall trend looks {trend['direction']}. This tool cannot give medical advice—"
                "please talk to your clinician for interpretation.")
    return "LLM summary placeholder."
