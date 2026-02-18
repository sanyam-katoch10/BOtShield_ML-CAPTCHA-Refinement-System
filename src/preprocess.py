"""Preprocess raw CAPTCHA images into normalized numpy arrays for model training.

Generates 2000 images per difficulty class (easy, medium, hard) with increasing
noise, distortion, and clutter parameters.
"""

import os

import numpy as np
from generator import generate_captcha

DATA_DIR = "data_preprocessed"
CLASSES = ["easy", "medium", "hard"]
IMAGES_PER_CLASS = 2000

DIFFICULTY_PARAMS = {
    "easy":   {"noise": 0.0, "dist": 0.0, "clutter": 0.0},
    "medium": {"noise": 0.3, "dist": 0.3, "clutter": 0.2},
    "hard":   {"noise": 0.7, "dist": 0.7, "clutter": 0.6},
}


def preprocess(data_dir: str = DATA_DIR, count: int = IMAGES_PER_CLASS) -> None:
    """Generate and save preprocessed CAPTCHA images for each difficulty class.

    Args:
        data_dir: Root directory for saving the preprocessed arrays.
        count: Number of images to generate per class.
    """
    os.makedirs(data_dir, exist_ok=True)
    for cls in CLASSES:
        os.makedirs(os.path.join(data_dir, cls), exist_ok=True)

    for cls in CLASSES:
        params = DIFFICULTY_PARAMS[cls]
        print(f"Generating {count} '{cls}' images...")
        for i in range(count):
            img, _ = generate_captcha(params["noise"], params["dist"], params["clutter"])
            arr = np.array(img.resize((200, 70))).astype("float32") / 255
            np.save(os.path.join(data_dir, cls, f"{i}.npy"), arr)
        print(f"  ✔ {cls} complete")

    print("Preprocessing finished.")


if __name__ == "__main__":
    preprocess()
