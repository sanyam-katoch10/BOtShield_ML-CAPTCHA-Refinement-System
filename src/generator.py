"""CAPTCHA image generator with configurable noise, distortion, and clutter."""

import random
import string

import cv2
import numpy as np
from captcha.image import ImageCaptcha
from PIL import Image


def random_text(length: int = 5) -> str:
    """Generate a random alphanumeric string for CAPTCHA text.

    Args:
        length: Number of characters to generate.

    Returns:
        A random string of uppercase letters and digits.
    """
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def cv2_to_pil(img: np.ndarray) -> Image.Image:
    """Convert an OpenCV BGR image to a PIL RGB Image."""
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


def pil_to_cv2(img: Image.Image) -> np.ndarray:
    """Convert a PIL RGB Image to an OpenCV BGR numpy array."""
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


def generate_captcha(
    noise: float = 0.0,
    dist: float = 0.0,
    clutter: float = 0.0,
    text: str | None = None,
) -> tuple[Image.Image, str]:
    """Generate a CAPTCHA image with configurable visual complexity.

    Args:
        noise: Noise intensity from 0.0 (none) to 1.0 (heavy salt-and-pepper).
        dist: Affine distortion intensity from 0.0 to 1.0.
        clutter: Random line clutter intensity from 0.0 to 1.0.
        text: Optional fixed CAPTCHA text; random if None.

    Returns:
        A tuple of (PIL Image, captcha_text).
    """
    if text is None:
        text = random_text()

    gen = ImageCaptcha(width=200, height=70)
    img = pil_to_cv2(gen.generate_image(text))
    h, w = img.shape[:2]

    if dist > 0:
        pts1 = np.float32([[0, 0], [w, 0], [0, h]])
        pts2 = np.float32([
            [random.randint(-5, 5), random.randint(-3, 3)],
            [w + random.randint(-5, 5), random.randint(-3, 3)],
            [random.randint(-5, 5), h + random.randint(-3, 3)],
        ])
        M = cv2.getAffineTransform(pts1, pts2)
        img = cv2.warpAffine(img, M, (w, h))

    if noise > 0:
        amt = int(150 * noise)
        for _ in range(amt):
            x = random.randint(0, w - 1)
            y = random.randint(0, h - 1)
            img[y, x] = [random.randint(0, 255) for _ in range(3)]

    if clutter > 0:
        cnt = int(6 * clutter)
        for _ in range(cnt):
            x1, y1 = random.randint(0, w), random.randint(0, h)
            x2, y2 = random.randint(0, w), random.randint(0, h)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            cv2.line(img, (x1, y1), (x2, y2), color, 1)

    return cv2_to_pil(img), text
