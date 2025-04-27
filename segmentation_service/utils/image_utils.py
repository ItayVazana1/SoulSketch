"""
Module: image_utils.py
Purpose: Utility functions for loading and basic processing of images.
Author: Itay Vazana (SoulSketch Project)
"""

import os
import cv2
import numpy as np


def load_image(image_path: str) -> np.ndarray:
    """
    Loads an image from a file path.

    Args:
        image_path (str): Path to the image file.

    Returns:
        np.ndarray: Loaded image in BGR format (OpenCV standard).

    Raises:
        FileNotFoundError: If the image does not exist or failed to load.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"❌ Image file not found: {image_path}")

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"❌ Failed to read image: {image_path}")

    return image


def save_image(image: np.ndarray, save_path: str) -> None:
    """
    Saves an image array to a file path.

    Args:
        image (np.ndarray): Image array to save.
        save_path (str): Destination file path.
    """
    directory = os.path.dirname(save_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    cv2.imwrite(save_path, image)


if __name__ == "__main__":
    # Example manual test
    try:
        img = load_image("shared/job_test/uploaded.png")
        save_image(img, "shared/job_test/output_test.png")
        print("✅ Test image loaded and saved successfully.")
    except Exception as e:
        print(f"❌ {e}")
