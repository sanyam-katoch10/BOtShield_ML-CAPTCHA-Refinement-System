# evaluate_captcha_html.py
import os
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

DATA_DIR = "data_preprocessed"
CLASSES = ["easy", "medium", "hard"]
MODEL_PATH = "models/captcha_model.keras"
OUTPUT_HTML = "evaluation_report.html"


X, y = [], []
for idx, cls in enumerate(CLASSES):
    folder = os.path.join(DATA_DIR, cls)
    for f in os.listdir(folder):
        arr = np.load(os.path.join(folder, f))
        X.append(arr)
        y.append(idx)

X = np.array(X).reshape(-1, 70, 200, 3).astype("float32")
y = np.array(y)
y_cat = to_categorical(y, num_classes=len(CLASSES))

print(f"Loaded {len(X)} images. Distribution per class: {np.bincount(y)}")


model = load_model(MODEL_PATH)


y_pred_prob = model.predict(X, verbose=1)
y_pred = np.argmax(y_pred_prob, axis=1)

acc = accuracy_score(y, y_pred)
report = classification_report(y, y_pred, target_names=CLASSES, output_dict=True)
cm = confusion_matrix(y, y_pred)

plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt='d', xticklabels=CLASSES, yticklabels=CLASSES, cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
cm_path = "confusion_matrix.png"
plt.savefig(cm_path)
plt.close()

html = f"""
<html>
<head>
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
<h2>Overall Accuracy: {acc*100:.2f}%</h2>

<h2>Classification Report</h2>
<table>
<tr>
<th>Class</th><th>Precision</th><th>Recall</th><th>F1-Score</th><th>Support</th>
</tr>
"""

for cls_name in CLASSES:
    html += f"<tr><td>{cls_name}</td><td>{report[cls_name]['precision']:.2f}</td><td>{report[cls_name]['recall']:.2f}</td><td>{report[cls_name]['f1-score']:.2f}</td><td>{int(report[cls_name]['support'])}</td></tr>"

html += f"""
</table>
<h2>Confusion Matrix</h2>
<img src="{cm_path}" alt="Confusion Matrix">
</body>
</html>
"""

Path(OUTPUT_HTML).write_text(html)
print(f"Evaluation report saved: {OUTPUT_HTML}")
