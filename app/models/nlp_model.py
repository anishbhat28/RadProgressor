import re
from typing import Dict, Tuple
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

_nlp_model = None
_tokenizer = None

def get_nlp_model():
    global _nlp_model, _tokenizer
    if _nlp_model is None:
        model_name = "emilyalsentzer/Bio_ClinicalBERT"
        _tokenizer = AutoTokenizer.from_pretrained(model_name)
        _nlp_model = AutoModelForSequenceClassification.from_pretrained(
            model_name, 
            num_labels=3
        )
        _nlp_model.eval()
    return _nlp_model, _tokenizer

def extract_sections(text: str) -> Dict[str, str]:
    findings_match = re.search(r'FINDINGS?:?\s*(.*?)(?=IMPRESSION|CONCLUSION|$)', text, re.IGNORECASE | re.DOTALL)
    impression_match = re.search(r'IMPRESSION?:?\s*(.*?)(?=CONCLUSION|$)', text, re.IGNORECASE | re.DOTALL)
    
    findings = findings_match.group(1).strip() if findings_match else ""
    impression = impression_match.group(1).strip() if impression_match else ""
    
    return {"findings": findings, "impression": impression}

def classify_change(text: str) -> Tuple[str, int]:
    model, tokenizer = get_nlp_model()
    
    change_words = {
        "improved": ["improved", "better", "resolved", "cleared", "decreased"],
        "worsened": ["worsened", "worse", "increased", "progression", "deteriorated", "new"]
    }
    
    text_lower = text.lower()
    
    improved_count = sum(1 for word in change_words["improved"] if word in text_lower)
    worsened_count = sum(1 for word in change_words["worsened"] if word in text_lower)
    
    if improved_count > worsened_count:
        return "improved", -1
    elif worsened_count > improved_count:
        return "worsened", 1
    else:
        return "stable", 0
