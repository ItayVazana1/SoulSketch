"""
Module: segmentor.py
Purpose: Perform segmentation on an image using a specified YOLO model.
Author: Itay Vazana (SoulSketch Project)
"""

from ultralytics import YOLO
from typing import List, Dict, Any
from segmentation_service.utils.image_utils import load_image
from segmentation_service.utils.model_loader import load_models

def segment_image(model: YOLO, image_path: str, conf_threshold: float = 0.5) -> List[Dict[str, Any]]:
    """
    Segments an image using the provided YOLOv8 model, returning masks and bounding boxes.

    Args:
        model (YOLO): A loaded YOLOv8 model.
        image_path (str): Path to the image to be segmented.
        conf_threshold (float): Minimum confidence score to keep a detection.

    Returns:
        List[Dict[str, Any]]: List of detected objects with mask and bbox data.
    """
    image = load_image(image_path)
    results = model.predict(source=image, save=False, conf=conf_threshold, verbose=False)

    if not results:
        return []

    result = results[0]
    output_objects = []

    if hasattr(result, 'masks') and result.masks is not None:
        masks = result.masks.data.cpu().numpy()
        boxes = result.boxes.xyxy.cpu().numpy()
        scores = result.boxes.conf.cpu().numpy()

        for i in range(len(masks)):
            obj = {
                "mask": masks[i],
                "bbox": boxes[i],
                "confidence": float(scores[i])
            }
            output_objects.append(obj)

    return output_objects

def extract_bboxes(model: YOLO, image: Any, conf_threshold: float = 0.25) -> List[Any]:
    """
    Extracts bounding boxes from a YOLOv8 model, without using masks.

    Args:
        model (YOLO): A loaded YOLOv8 model.
        image (np.ndarray): Loaded BGR image.
        conf_threshold (float): Minimum confidence score to keep a detection.

    Returns:
        List[np.ndarray]: List of bounding boxes [x_min, y_min, x_max, y_max].
    """
    results = model.predict(source=image, save=False, conf=conf_threshold, verbose=False)

    bboxes = []
    if not results:
        return []

    for r in results:
        if hasattr(r, 'boxes') and r.boxes is not None:
            boxes = r.boxes.xyxy.cpu().numpy()
            bboxes.extend(boxes)

    return bboxes

if __name__ == "__main__":
    models = load_models(models_base_path="models")
    nano_v08_model = models["nano"]["v08"]

    # Example: Using segment_image (with masks)
    objects = segment_image(nano_v08_model, image_path="shared/job_test/uploaded.png")
    print(f"🔵 Objects detected (with masks): {len(objects)}")

    # Example: Using extract_bboxes (only bounding boxes)
    image = load_image("shared/job_test/uploaded.png")
    boxes = extract_bboxes(nano_v08_model, image)
    print(f"🔵 Bounding boxes extracted: {len(boxes)}")
