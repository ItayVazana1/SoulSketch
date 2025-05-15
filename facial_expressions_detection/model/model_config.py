"""
Project: SoulSketch
File: facial_expressions_detection/model/model_config.py
Authors: Itay Vazana & Oriya Even Chen

Description:
Configuration file for the facial expression detection module.
Defines model path, detection thresholds, and valid expression labels.
"""

import sys
from pathlib import Path

# ==== Project Root Resolution ====
PROJECT_ROOT = Path(__file__).resolve().parent
while PROJECT_ROOT.name != "SoulSketch":
    if PROJECT_ROOT.parent == PROJECT_ROOT:
        break
    PROJECT_ROOT = PROJECT_ROOT.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==== Model Path ====
# Path to the trained YOLOv8 model for facial expression detection
MODEL_PATH = "model/Yolo11s_FED_trained.pt"

# ==== Detection Thresholds ====
# Confidence and IoU settings used during inference
CONFIDENCE_THRESHOLD = 0.25
IOU_THRESHOLD = 0.7

# ==== Valid Expression Labels ====
# Facial expression labels used during model training
FACIAL_EXPRESSIONS = [
    "angry_face", "happy_face", "sad_face", "neutral_face",
    "drawn_face", "hollow_eyes", "large_eyes", "angry_eyes",
    "dot_eyes", "far_eyes", "one_pupil"
]
