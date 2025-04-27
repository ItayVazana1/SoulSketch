"""
Module: iou_utils.py
Purpose: Calculate IoU and filter duplicate bounding boxes based on overlap.
Author: Itay Vazana (SoulSketch Project)
"""

import numpy as np
from typing import List, Tuple

def calculate_iou(boxA: np.ndarray, boxB: np.ndarray) -> float:
    """
    Calculate Intersection over Union (IoU) between two bounding boxes.

    Args:
        boxA (np.ndarray): Bounding box A [x_min, y_min, x_max, y_max].
        boxB (np.ndarray): Bounding box B [x_min, y_min, x_max, y_max].

    Returns:
        float: IoU value (0.0 - 1.0).
    """
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    interArea = max(0, xB - xA) * max(0, yB - yA)
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

    iou = interArea / float(boxAArea + boxBArea - interArea + 1e-6)
    return iou

def filter_duplicates(
    boxes_sources: List[Tuple[np.ndarray, str]],
    iou_threshold: float = 0.5
) -> List[Tuple[np.ndarray, str]]:
    """
    Filter out duplicate bounding boxes based on IoU threshold.

    Args:
        boxes_sources (List[Tuple[np.ndarray, str]]): List of (bbox, model_source_tag).
        iou_threshold (float): IoU threshold for considering two boxes as duplicates.

    Returns:
        List[Tuple[np.ndarray, str]]: Filtered list of boxes.
    """
    filtered = []
    for box_src in boxes_sources:
        box, src = box_src
        duplicate = False
        for kept_box, _ in filtered:
            if calculate_iou(box, kept_box) > iou_threshold:
                duplicate = True
                break
        if not duplicate:
            filtered.append((box, src))
    return filtered

if __name__ == "__main__":
    # No standalone test here — used internally
    pass
