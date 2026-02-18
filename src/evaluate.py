"""Evaluate the trained CAPTCHA difficulty CNN and generate an HTML report
with classification metrics and a confusion matrix heatmap."""

import os

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical

DATA_DIR = "data_preprocessed"
CLASSES = ["easy", "medium", "hard"]
MODEL_PATH = "models/captcha_model.keras"
OUTPUT_HTML = "evaluation_report.html"


def load_dataset(data_dir: str = DATA_DIR) -> tuple[np.ndarray, np.ndarray]:
    """Load all preprocessed images and labels.

    Returns:
        A tuple of (images_array, integer_labels).
    """
    X, y = [], []
    for idx, cls in enumerate(CLASSES):
        folder = os.path.join(data_dir, cls)
        for f in os.listdir(folder):
            arr = np.load(os.path.join(folder, f))
            X.append(arr)
            y.append(idx)

    X = np.array(X).reshape(-1, 70, 200, 3).astype("float32")
    y = np.array(y)
    return X, y


def evaluate_model(X: np.ndarray, y: np.ndarray) -> tuple[float, dict, np.ndarray]:
    """Run predictions and compute evaluation metrics.

    Returns:
        A tuple of (accuracy, classification_report_dict, confusion_matrix).
    """
    model = load_model(MODEL_PATH)
    y_pred_prob = model.predict(X, verbose=1)
    y_pred = np.argmax(y_pred_prob, axis=1)

    acc = accuracy_score(y, y_pred)
    report = classification_report(y, y_pred, target_names=CLASSES, output_dict=True)
    cm = confusion_matrix(y, y_pred)
    return acc, report, cm


def save_confusion_matrix(cm: np.ndarray, output_path: str = "confusion_matrix.png") -> str:
    """Plot and save the confusion matrix as a PNG heatmap."""
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', xticklabels=CLASSES, yticklabels=CLASSES, cmap="Blues")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return output_path


def generate_html_report(acc: float, report: dict, cm_path: str) -> None:
    """Write an HTML evaluation report to disk."""
    rows = ""
    for cls_name in CLASSES:
        r = report[cls_name]
        rows += (
            f"<tr><td>{cls_name}</td>"
            f"<td>{r['precision']:.2f}</td>"
            f"<td>{r['recall']:.2f}</td>"
            f"<td>{r['f1-score']:.2f}</td>"
            f"<td>{int(r['support'])}</td></tr>\n"
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>CAPTCHA Model Evaluation Report</title>
<style>
body {{ font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px; }}
h1 {{ color: #2e6c80; }}
table {{ border-collapse: collapse; width: 60%; margin-bottom: 20px; }}
th, td {{ border: 1px solid #999; padding: 8px; text-align: center; }}
th {{ background-color: #2e6c80; color: white; }}
tr:nth-child(even) {{ background-color: #f2f2f2; }}
img {{ max-width: 500px; margin-top: 10px; }}
</style>
</head>
<body>
<h1>ML CAPTCHA Model Evaluation</h1>
<h2>Overall Accuracy: {acc * 100:.2f}%</h2>
<h2>Classification Report</h2>
<table>
<tr><th>Class</th><th>Precision</th><th>Recall</th><th>F1-Score</th><th>Support</th></tr>
{rows}
</table>
<h2>Confusion Matrix</h2>
<img src="{cm_path}" alt="Confusion Matrix">
</body>
</html>"""

    Path(OUTPUT_HTML).write_text(html, encoding="utf-8")
    print(f"Evaluation report saved: {OUTPUT_HTML}")


if __name__ == "__main__":
    X, y = load_dataset()
    print(f"Loaded {len(X)} images. Distribution per class: {np.bincount(y)}")

    acc, report, cm = evaluate_model(X, y)
    cm_path = save_confusion_matrix(cm)
    generate_html_report(acc, report, cm_path)
