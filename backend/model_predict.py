import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import torch
import cv2
import numpy as np
from torchvision import transforms
from model.unet_model import UNet
from PIL import Image

# Загружаем модель
model = UNet(in_channels=3)
model.load_state_dict(torch.load("../model/model.pth", map_location=torch.device('cpu')))
model.eval()

transform = transforms.Compose([
    transforms.Resize((512, 512)),
    transforms.ToTensor(),
])

def analyze_image(image_path):
    image = Image.open(image_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(input_tensor)

    mask = output.squeeze().numpy()
    mask_binary = (mask > 0.5).astype(np.uint8)

    coords = cv2.findNonZero(mask_binary * 255)
    if coords is not None:
        x, y, w, h = cv2.boundingRect(coords)
        tumor_coords = [(int(x), int(y)), (int(x + w), int(y + h))]
    else:
        tumor_coords = []

    confidence = float(mask.mean())
    risk = "high" if confidence > 0.5 else "low"

    return {
        'tumor_coordinates': tumor_coords,
        'ai_confidence': round(confidence, 2),
        'risk_level': risk
    }
