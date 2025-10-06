import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision.models import densenet121, resnet50
from PIL import Image
import numpy as np
from typing import Dict, Tuple
from app.config import CHEST_XRAY_LABELS

class ChestXRayModel(nn.Module):
    def __init__(self, num_classes: int = 5, model_name: str = "densenet121"):
        super().__init__()
        if model_name == "densenet121":
            self.backbone = densenet121(pretrained=True)
            self.backbone.classifier = nn.Linear(self.backbone.classifier.in_features, num_classes)
        elif model_name == "resnet50":
            self.backbone = resnet50(pretrained=True)
            self.backbone.fc = nn.Linear(self.backbone.fc.in_features, num_classes)
        else:
            raise ValueError(f"Unsupported model: {model_name}")
        
        self.num_classes = num_classes
        self.labels = CHEST_XRAY_LABELS

    def forward(self, x):
        return self.backbone(x)

_cv_model = None

def get_cv_model() -> ChestXRayModel:
    global _cv_model
    if _cv_model is None:
        _cv_model = ChestXRayModel()
        _cv_model.eval()
    return _cv_model

def preprocess_image(image: Image.Image) -> torch.Tensor:
    transform = transforms.Compose([
        transforms.Grayscale(num_output_channels=3),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return transform(image).unsqueeze(0)

def predict(image: Image.Image) -> Tuple[Dict[str, float], float]:
    model = get_cv_model()
    tensor = preprocess_image(image)
    
    with torch.no_grad():
        logits = model(tensor)
        probs = torch.sigmoid(logits).squeeze().numpy()
    
    labels = {label: float(prob) for label, prob in zip(CHEST_XRAY_LABELS, probs)}
    severity_score = float(max(probs))
    
    return labels, severity_score
