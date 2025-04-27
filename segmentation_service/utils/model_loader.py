"""
Module: model_loader.py
Purpose: Load YOLO segmentation models organized by suffix.
Author: Itay Vazana (SoulSketch Project)
"""

import os
from ultralytics import YOLO

def load_models(models_base_path: str) -> dict:
    """
    Loads YOLOv8 segmentation models from the given base path.

    Args:
        models_base_path (str): Path to the 'models/' directory.

    Returns:
        dict: Dictionary structured as {model_suffix: YOLO model}
    """
    layers = {
        "nano": "n",
        "small": "s"
        #"medium": "m",
    }
    versions = ["v08", "v11", "v12"]
    models = {}

    for layer_name, layer_tag in layers.items():
        layer_path = os.path.join(models_base_path, layer_name)

        for version in versions:
            model_filename = f"Yolo_{version}_{layer_name}-seg.pt"
            model_path = os.path.join(layer_path, model_filename)

            if os.path.exists(model_path):
                try:
                    model = YOLO(model_path)
                    suffix = f"{layer_tag}{version[1:]}"  # e.g., n08, s11, m12
                    models[suffix] = model
                    print(f"✅ Loaded model: {suffix}")
                except Exception as e:
                    print(f"❌ Failed to load model {model_path}: {e}")
            else:
                print(f"⚠️ Model file not found: {model_path}")

    return models


if __name__ == "__main__":
    models = load_models(models_base_path="models")
    print(f"🔵 Total models loaded: {len(models)}")
