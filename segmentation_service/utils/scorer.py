"""
Module: scorer.py
Purpose: Evaluate segmentation outputs and assign a quality score.
Author: Itay Vazana (SoulSketch Project)
"""

from typing import List, Dict, Any

def score_segmentation(objects: List[Dict[str, Any]]) -> float:
    """
    Computes a quality score for a list of detected objects.

    Scoring Strategy:
    - Prefers a reasonable number of objects (not too few, not too many)
    - Rewards larger object areas
    - Rewards higher confidence scores

    Args:
        objects (List[Dict[str, Any]]): List of segmented objects.

    Returns:
        float: Quality score (higher is better).
    """
    if not objects:
        return 0.0

    num_objects = len(objects)
    avg_confidence = sum(obj["confidence"] for obj in objects) / num_objects

    # Estimate average object area
    total_area = 0
    for obj in objects:
        x_min, y_min, x_max, y_max = obj["bbox"]
        width = max(0, x_max - x_min)
        height = max(0, y_max - y_min)
        area = width * height
        total_area += area

    avg_area = total_area / num_objects if num_objects > 0 else 0

    # Define heuristics for "good" segmentation
    # Weight: 50% confidence, 30% area size, 20% number of objects normalization
    confidence_score = avg_confidence
    area_score = min(avg_area / (256 * 256), 1.0)  # Normalize area (assuming a 256x256 object is "large")
    object_count_score = 1.0 if 2 <= num_objects <= 10 else 0.5  # Prefer drawings with 2-10 objects

    final_score = (0.5 * confidence_score) + (0.3 * area_score) + (0.2 * object_count_score)

    return final_score


if __name__ == "__main__":
    # Example manual test
    fake_objects = [
        {"bbox": [10, 10, 50, 50], "confidence": 0.85},
        {"bbox": [60, 60, 120, 120], "confidence": 0.90}
    ]

    score = score_segmentation(fake_objects)
    print(f"🔵 Example segmentation score: {score:.3f}")
