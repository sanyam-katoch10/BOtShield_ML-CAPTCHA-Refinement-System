"""CAPTCHA difficulty refinement engine — iteratively adjusts generation
parameters until the CNN classifier predicts the desired difficulty level."""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from generator import generate_captcha

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(_BASE_DIR, "..", "models", "captcha_model.keras")
CLASSES = ["easy", "medium", "hard"]

model = load_model(MODEL_PATH, compile=False, safe_mode=False)


def predict(img: Image.Image) -> tuple[str, float]:
    """Predict the difficulty level of a CAPTCHA image.

    Args:
        img: PIL Image of the CAPTCHA to classify.

    Returns:
        A tuple of (predicted_class, confidence_score).
    """
    arr = np.array(img.resize((200, 70))).astype("float32") / 255
    arr = np.expand_dims(arr, 0)
    probs = model.predict(arr, verbose=0)[0]
    idx = np.argmax(probs)
    return CLASSES[idx], float(probs[idx])


def refine(target: str = "medium", steps: int = 4) -> tuple[Image.Image, str, str]:
    """Generate a CAPTCHA and iteratively refine it to match the target difficulty.

    Args:
        target: Desired difficulty level — "easy", "medium", or "hard".
        steps: Maximum number of refinement iterations.

    Returns:
        A tuple of (captcha_image, captcha_text, predicted_difficulty).
    """
    difficulty_map = {"easy": 0, "medium": 1, "hard": 2}
    noise, dist, clutter = 0.3, 0.3, 0.3

    for _ in range(steps):
        img, text = generate_captcha(noise, dist, clutter)
        pred, _ = predict(img)
        if pred == target:
            return img, text, pred
        if difficulty_map[pred] < difficulty_map[target]:
            noise = min(1, noise + 0.15)
            dist = min(1, dist + 0.1)
            clutter = min(1, clutter + 0.1)
        else:
            noise = max(0, noise - 0.15)
            dist = max(0, dist - 0.1)
            clutter = max(0, clutter - 0.1)

    return img, text, pred


if __name__ == "__main__":
    img, text, pred = refine("medium")
    print("Generated CAPTCHA text:", text)
    print("Predicted difficulty:", pred)
    img.show()
