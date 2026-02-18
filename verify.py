"""Verify preprocessed CAPTCHA data by visualizing sample images from each difficulty class."""

import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

DATA_DIR = "data_preprocessed"
CLASSES = ["easy", "medium", "hard"]


def visualize_samples(data_dir: str = DATA_DIR, num_samples: int = 6) -> None:
    """Display sample preprocessed images from each difficulty class.

    Args:
        data_dir: Path to the directory containing preprocessed data folders.
        num_samples: Number of sample images to display per class.
    """
    for cls in CLASSES:
        folder = os.path.join(data_dir, cls)
        files = os.listdir(folder)[:num_samples]

        print(f"\nShowing samples from {cls}:")
        plt.figure(figsize=(12, 4))
        for i, f in enumerate(files):
            arr = np.load(os.path.join(folder, f))
            plt.subplot(1, num_samples, i + 1)
            plt.imshow(arr.astype("uint8"))
            plt.axis("off")
        plt.suptitle(f"Class: {cls.upper()}", fontsize=14, fontweight="bold")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    visualize_samples()
