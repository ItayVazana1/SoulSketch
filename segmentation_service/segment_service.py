"""
Module: segment_service.py
Purpose: Main segmentation service loop for SoulSketch project — based on bounding boxes.
Author: Itay Vazana (SoulSketch Project)
"""

import os
import time
import yaml
from typing import List

from segmentation_service.utils.model_loader import load_models
from segmentation_service.utils.image_utils import load_image
from segmentation_service.utils.segmentor import extract_bboxes
from segmentation_service.utils.crop_saver import save_crop_from_bbox
from segmentation_service.utils.iou_utils import filter_duplicates

def load_config(config_path: str = "config.yaml") -> dict:
    """
    Loads the configuration YAML file.

    Args:
        config_path (str): Path to the configuration YAML file.

    Returns:
        dict: Loaded configuration dictionary.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"❌ Config file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def find_latest_job_dir(base_shared_dir: str) -> str:
    """
    Finds the latest job_<uuid> directory inside the base shared directory.

    Args:
        base_shared_dir (str): Path to the base shared directory.

    Returns:
        str: Full path to the latest job directory.
    """
    job_dirs = [
        os.path.join(base_shared_dir, d)
        for d in os.listdir(base_shared_dir)
        if os.path.isdir(os.path.join(base_shared_dir, d)) and d.startswith("job_")
    ]

    if not job_dirs:
        raise FileNotFoundError(f"❌ No job directories found in {base_shared_dir}")

    job_dirs.sort(key=lambda d: os.path.getmtime(d))
    latest_job_dir = job_dirs[-1]
    print(f"📂 Latest job detected: {latest_job_dir}")
    return latest_job_dir

def wait_for_uploaded_image(shared_dir: str, valid_extensions: List[str], check_interval: int) -> str:
    """
    Waits until an image file appears in the shared directory.

    Args:
        shared_dir (str): Path to the shared/job_<uuid>/ folder.
        valid_extensions (List[str]): List of accepted image file extensions.
        check_interval (int): Seconds between each check.

    Returns:
        str: Path to the detected image file.
    """
    print(f"🔵 Waiting for uploaded image in: {shared_dir} ...")
    while True:
        for file in os.listdir(shared_dir):
            if any(file.lower().endswith(ext) for ext in valid_extensions):
                image_path = os.path.join(shared_dir, file)
                print(f"📥 Image detected: {image_path}")
                return image_path
        time.sleep(check_interval)

def run_segmentation_service():
    """
    Runs the main segmentation service loop based on bounding boxes.
    """
    print("🧠 Segmentation Service Started...")

    config = load_config()

    base_shared_dir = config["base_shared_dir"]
    models_base_path = config["models_dir"]
    output_subdir_name = config.get("output_subdir", "objects")
    valid_extensions = [".png", ".jpg", ".jpeg"]
    check_interval = config.get("check_interval_seconds", 5)
    conf_threshold = config.get("confidence_threshold", 0.25)
    iou_threshold = config.get("iou_threshold", 0.5)

    # Load models
    models = load_models(models_base_path=models_base_path)

    while True:
        try:
            shared_dir = find_latest_job_dir(base_shared_dir)
            output_dir = os.path.join(shared_dir, output_subdir_name)

            # Check if objects folder already exists and is non-empty
            if os.path.exists(output_dir) and os.listdir(output_dir):
                print(f"⚠️ Objects already exist for {shared_dir}. Skipping...")
                time.sleep(check_interval)
                continue

            image_path = wait_for_uploaded_image(shared_dir, valid_extensions, check_interval)
            image = load_image(image_path)

            all_boxes = []

            # Run all models
            for model_suffix, model in models.items():
                bboxes = extract_bboxes(model, image, conf_threshold=conf_threshold)
                for bbox in bboxes:
                    all_boxes.append((bbox, model_suffix))

            print(f"🧠 Total detections before filtering: {len(all_boxes)}")

            # Filter duplicate boxes
            filtered_boxes = filter_duplicates(all_boxes, iou_threshold=iou_threshold)
            print(f"🔍 After filtering duplicates: {len(filtered_boxes)} objects")

            # Prepare output directory
            os.makedirs(output_dir, exist_ok=True)

            # Save crops
            for idx, (bbox, source_tag) in enumerate(filtered_boxes, start=1):
                save_filename = f"obj_{idx:03}_{source_tag}.png"
                save_path = os.path.join(output_dir, save_filename)
                save_crop_from_bbox(image, bbox, save_path)

            print("✅ Segmentation for job completed successfully!\n")

        except Exception as e:
            print(f"❌ Error during segmentation service: {e}")
            time.sleep(5)


if __name__ == "__main__":
    run_segmentation_service()
