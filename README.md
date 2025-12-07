
<p align="center">
  <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" width="120"/>
</p>

<h1 align="center">✨ ML-Enhanced CAPTCHA Refinement System ✨</h1>
<h3 align="center">AI-Powered Adaptive CAPTCHA Generator & Difficulty Classifier</h3>

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge"/></a>
  <a href="#"><img src="https://img.shields.io/badge/TensorFlow-Keras-orange?style=for-the-badge"/></a>
  <a href="#"><img src="https://img.shields.io/badge/Streamlit-Live_App-ff4b4b?style=for-the-badge"/></a>
  <a href="#"><img src="https://img.shields.io/badge/OpenCV-Image_Processing-green?style=for-the-badge"/></a>
  <a href="#"><img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge"/></a>
</p>

---

## 🌐 Live Demo

<p align="center">
  🔗 **Coming Soon** — Your Streamlit App URL will appear here
</p>

---

## 🎯 Project Overview

The **ML-Enhanced CAPTCHA Refinement System** generates CAPTCHAs and automatically adjusts difficulty using a **CNN classifier**, ensuring:

<div align="center">
  <span style="color:#00bfff">✅ Human readability</span>  
  <span style="color:#ff8c00">✅ Bot resistance</span>  
  <span style="color:#32cd32">✅ Security & usability</span>  
</div>

The system dynamically modulates **noise**, **distortion**, and **clutter** until the CAPTCHA matches the desired difficulty: **Easy**, **Medium**, or **Hard**.

---

## ✨ Features

<details>
<summary>🔐 Smart CAPTCHA Generator</summary>

* Adjustable noise, distortion, and clutter
* Random text generation
* Fully image-based CAPTCHA pipeline

</details>

<details>
<summary>🤖 CNN Difficulty Classifier</summary>

* Trained on 6,000 synthetic images
* Achieves high accuracy (>90%)
* TensorFlow/Keras-based CNN

</details>

<details>
<summary>🔄 Adaptive Refinement Loop</summary>

* Predict → Adjust → Re-generate → Repeat
* Ensures output matches target difficulty
* Optimized for real-time applications

</details>

<details>
<summary>🎨 Streamlit Web Interface</summary>

* Dark-themed, modern UI
* Sliders for live parameter adjustment
* Instant CAPTCHA preview and download
* Smooth, responsive, real-time experience

</details>

---

## 🧠 Architecture Diagram

```mermaid
flowchart LR
A[CAPTCHA Generation] --> B[CNN Classifier]
B --> C[Difficulty Check]
C --> D[Adjust Noise / Distortion / Clutter]
D --> E[Final CAPTCHA Output]
```

---

## 📁 Project Structure

```
ML-CAPTCHA-Refinement/
│
├── src/
│   ├── generator.py        # CAPTCHA generation
│   ├── refine_m.py         # Refinement logic
│   ├── train_model.py      # CNN training
│   ├── app.py              # Streamlit app
│
├── models/
│   └── captcha_model.keras # Pretrained ML model
│
├── data_preprocessed/      # Preprocessed CAPTCHA dataset
├── requirements.txt
└── README.md
```

---

## 🛠 Tech Stack

| Component         | Technology                       |
| ----------------- | -------------------------------- |
| Frontend UI       | Streamlit                        |
| ML Framework      | TensorFlow / Keras               |
| Image Processing  | OpenCV, Pillow                   |
| CAPTCHA Generator | Python `captcha` library         |
| Deployment        | Streamlit Cloud                  |
| Dataset Creation  | Python-based synthetic generator |

---

## 🚀 Installation & Setup

<details>
<summary>Click to expand</summary>

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/ML-CAPTCHA-Refinement.git
cd ML-CAPTCHA-Refinement
```

### 2️⃣ Create Virtual Environment

```bash
# Windows
py -3.11 -m venv venv
venv\Scripts\activate.ps1

# macOS/Linux
python3.11 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4️⃣ Run Streamlit App

```bash
streamlit run src/app.py
```

</details>

---

## 🧪 Machine Learning Details

<details>
<summary>Click to expand</summary>

### Model

Lightweight **CNN** for CAPTCHA difficulty classification.

### Training Highlights

* Dataset: 6,000 labeled images
* Layers: Conv2D + MaxPooling + BatchNorm + Dense
* Optimizer: Adam
* Loss: Categorical Crossentropy
* Regularization: Dropout
* Validation Accuracy: >90%

### Refinement Logic

1. Generate CAPTCHA
2. Predict difficulty
3. Adjust noise/distortion/clutter
4. Repeat until target difficulty is achieved

</details>

---

## 📸 Screenshots

<details>
<summary>Click to expand</summary>

### Generator UI

*(Add screenshot here)*

### Refinement Mode

*(Add screenshot here)*

</details>

---

## 💡 Future Enhancements

* Reinforcement learning-based difficulty tuning
* Human feedback loop integration
* Audio CAPTCHAs & image puzzles
* Adversarial bot-resistance testing

---

## 👨‍💻 Author

**Sanyam Katoch**
ML • AI • Computer Vision
[GitHub](https://github.com/sanyam-katoch10)
