"""
BotShield API — FastAPI wrapper for the CAPTCHA refinement model.

Run with:
    cd src
    py -3 -m uvicorn api:app --reload --port 8000

Endpoints:
    GET  /generate?difficulty=medium  → generates a refined CAPTCHA
    POST /predict                     → predicts difficulty of an uploaded image
    GET  /health                      → health check
"""

import os
import sys
import base64
import shutil
from io import BytesIO

import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

# ── Optional OCR engine + Auto-Detection ──
try:
    import pytesseract
    OCR_AVAILABLE = True

    # Check for Tesseract binary
    tess_path = shutil.which("tesseract")
    if not tess_path:
        # Common Windows installation paths
        common_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe"),
        ]
        for path in common_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                OCR_AVAILABLE = True
                break
        else:
             # If strictly needed, we can set OCR_AVAILABLE = False here,
             # but keeping it True allows 'tesseract not found' error to be caught in ocr_text()
             pass
except ImportError:
    OCR_AVAILABLE = False

# ── Ensure sibling imports work ──
sys.path.insert(0, os.path.dirname(__file__))

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from refine_m import refine, predict
from generator import generate_captcha

# ══════════════════════════════════════════════════════════════════════════════
#  APP SETUP
# ══════════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="BotShield API",
    description="ML-Enhanced CAPTCHA Generation & Difficulty Prediction",
    version="1.0.0",
)

# Allow browser extension to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def img_to_base64(img: Image.Image) -> str:
    """Convert a PIL Image to a base64-encoded PNG string."""
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def ocr_text(img: Image.Image) -> str:
    """Try to extract text from a CAPTCHA image using Tesseract OCR."""
    if not OCR_AVAILABLE:
        return "(Install pytesseract + Tesseract-OCR)"
    try:
        # Preprocess: grayscale → threshold → invert for better OCR
        arr = np.array(img.convert("L"))
        _, thresh = cv2.threshold(arr, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        # Run Tesseract with CAPTCHA-friendly config
        config = "--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        text = pytesseract.image_to_string(thresh, config=config).strip()
        return text if text else "(unreadable)"
    except Exception:
        return "(Tesseract binary not found)"


# ══════════════════════════════════════════════════════════════════════════════
#  ENDPOINTS
# ══════════════════════════════════════════════════════════════════════════════

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "online", "model": "CNN v1"}


@app.get("/generate")
def generate(difficulty: str = "medium"):
    """
    Generate a CAPTCHA image refined to the target difficulty.

    Query params:
        difficulty: "easy" | "medium" | "hard"

    Returns:
        JSON with base64 image, captcha text, difficulty, and confidence.
    """
    img, text, level = refine(difficulty)
    pred_label, confidence = predict(img)

    return {
        "image": img_to_base64(img),
        "text": text,
        "difficulty": level,
        "predicted": pred_label,
        "confidence": round(float(confidence), 4),
    }


@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    """
    Predict the difficulty of an uploaded CAPTCHA image.

    Body:
        file: Image file (PNG/JPG)

    Returns:
        JSON with predicted difficulty, confidence, and recognized text.
    """
    contents = await file.read()
    img = Image.open(BytesIO(contents)).convert("RGB")
    pred_label, confidence = predict(img)
    text = ocr_text(img)

    return {
        "difficulty": pred_label,
        "confidence": round(float(confidence), 4),
        "text": text,
    }
