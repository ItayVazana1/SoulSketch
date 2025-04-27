"""
Module: crop_saver.py
Purpose: Save object crops from bounding boxes (without masks).
Author: Itay Vazana (SoulSketch Project)
"""

import os
import numpy as np
import cv2
from typing import List, Dict, Any
from segmentation_service.utils.image_utils import save_image, load_image

def save_crops(
    objects: List[Dict[str, Any]],
    image_path: str,
    output_dir: str,
    layer_tag: str,
    model_version: str,
    starting_index: int = 0
) -> int:
    """
    Save crops based on segmentation objects that contain masks and bounding boxes.
    (Original segmentation flow — not used for simple bbox cropping.)

    Args:
        objects (List[Dict[str, Any]]): List of detected objects (with masks).
        image_path (str): Path to the original input image.
        output_dir (str): Directory to save the crops.
        layer_tag (str): Layer tag (N/S/M) to include in filename.
        model_version (str): YOLO model version (8/10/12).
        starting_index (int): Starting object index for naming.

    Returns:
        int: Updated index after saving all crops.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image = load_image(image_path)

    for i, obj in enumerate(objects):
        if "mask" not in obj or "bbox" not in obj:
            print(f"⚠️ Skipping invalid object structure: {obj}")
            continue

        mask = obj["mask"]
        bbox = obj["bbox"]

        x_min, y_min, x_max, y_max = map(int, bbox)

        if x_min >= x_max or y_min >= y_max:
            print(f"⚠️ Skipping invalid bbox: {bbox}")
            continue

        crop = image[y_min:y_max, x_min:x_max]
        if crop.size == 0:
            print(f"⚠️ Skipping empty crop for bbox: {bbox}")
            continue

        # Apply mask inside the bounding box (optional)
        mask_cropped = mask[y_min:y_max, x_min:x_max]
        mask_resized = cv2.resize(mask_cropped, (crop.shape[1], crop.shape[0]))
        mask_binary = (mask_resized > 0.5).astype(np.uint8)

        crop = cv2.bitwise_and(crop, crop, mask=mask_binary)

        obj_id = starting_index + i
        filename = f"obj_{obj_id}_Yolo_{model_version}_{layer_tag}.png"
        save_path = os.path.join(output_dir, filename)

        save_image(crop, save_path)

    return starting_index + len(objects)

def save_crop_from_bbox(image: np.ndarray, bbox: np.ndarray, save_path: str) -> None:
    """
    Save a simple crop from a bounding box area (no mask).

    Args:
        image (np.ndarray): The original loaded image (BGR).
        bbox (np.ndarray): Bounding box [x_min, y_min, x_max, y_max].
        save_path (str): Full path to save the cropped image.
    """
    x_min, y_min, x_max, y_max = map(int, bbox)

    # Sanity check for bbox coordinates
    h, w = image.shape[:2]
    x_min = max(0, min(w - 1, x_min))
    y_min = max(0, min(h - 1, y_min))
    x_max = max(0, min(w, x_max))
    y_max = max(0, min(h, y_max))

    if x_min >= x_max or y_min >= y_max:
        print(f"⚠️ Skipping invalid bbox: {bbox}")
        return

    crop = image[y_min:y_max, x_min:x_max]

    if crop.size == 0:
        print(f"⚠️ Skipping empty crop for bbox: {bbox}")
        return

    save_image(crop, save_path)
    print(f"✅ Saved crop to: {save_path}")

if __name__ == "__main__":
    # No standalone test here
    pass
