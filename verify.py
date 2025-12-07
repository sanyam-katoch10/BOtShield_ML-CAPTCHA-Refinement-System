
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

DATA_DIR = "data_preprocessed"
CLASSES = ["easy", "medium", "hard"]

for cls in CLASSES:
    folder = os.path.join(DATA_DIR, cls)
    files = os.listdir(folder)[:6]

    print(f"\nShowing samples from {cls}:")
    plt.figure(figsize=(12, 4))
    for i, f in enumerate(files):
        arr = np.load(os.path.join(folder, f))
        plt.subplot(1, 6, i+1)
        plt.imshow(arr.astype("uint8"))
        plt.axis("off")
    plt.show()

