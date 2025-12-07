
<p align="center">
  <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" width="100"/>
</p>

<h1 align="center">ML-Enhanced CAPTCHA Refinement System</h1>
<h3 align="center">AI-Powered Adaptive CAPTCHA Generator & Difficulty Classifier</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/TensorFlow-Keras-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Streamlit-Live_App-ff4b4b?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/OpenCV-Image_Processing-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge"/>
</p>

---

## 🌐 Live Demo

<p align="center">
  🔗 **Coming Soon** — Your Streamlit App URL will appear here
</p>

---

## 🎯 Project Overview

The **ML-Enhanced CAPTCHA Refinement System** intelligently generates CAPTCHAs and automatically adjusts difficulty using a **CNN classifier**. It ensures a perfect balance between:

✅ Human readability
✅ Bot resistance
✅ Security + usability

The system dynamically modulates **noise**, **distortion**, and **clutter** until the CAPTCHA matches the desired difficulty level: **Easy**, **Medium**, or **Hard**.

---

## ✨ Features

### 🔐 Smart CAPTCHA Generator

* Adjustable noise, distortion, and clutter
* Random text generation
* Fully image-based CAPTCHA pipeline

### 🤖 CNN Difficulty Classifier

* Trained on 6,000 synthetic images
* Achieves high accuracy (>90%)
* TensorFlow/Keras-based model

### 🔄 Adaptive Refinement Loop

* Predict → Adjust → Re-generate → Repeat
* Ensures the output matches the target difficulty
* Optimized for real-time applications

### 🎨 Streamlit Web Interface

* Dark-themed, intuitive UI
* Live sliders for parameter tuning
* Instant CAPTCHA preview and download
* Smooth and responsive experience

---

## 🧠 Architecture Diagram

```
CAPTCHA Generation → CNN Classifier → Difficulty Check → Adjust Noise/Distortion/Clutter → OUTPUT
```

---

## 📁 Project Structure

```
ML-CAPTCHA-Refinement/
│
├── src/
│   ├── generator.py        # CAPTCHA generation script
│   ├── refine_m.py         # Difficulty refinement logic
│   ├── train_model.py      # CNN training script
│   ├── app.py              # Streamlit web app
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
| CAPTCHA Generator | `captcha` library                |
| Deployment        | Streamlit Cloud                  |
| Dataset Creation  | Python-based synthetic generator |

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/ML-CAPTCHA-Refinement.git
cd ML-CAPTCHA-Refinement
```

### 2️⃣ Create a Virtual Environment

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

### 4️⃣ Run the Streamlit App

```bash
streamlit run src/app.py
```

---

## 🧪 Machine Learning Details

### Model

A **Convolutional Neural Network (CNN)** trained on synthetic CAPTCHA images for difficulty classification.

### Training Highlights

* Dataset: 6,000 images labeled as Easy/Medium/Hard
* CNN Layers: Conv2D + MaxPooling + BatchNorm + Dense
* Optimizer: Adam
* Loss: Categorical Crossentropy
* Regularization: Dropout for overfitting prevention
* Achieved Accuracy: >90% validation accuracy

### Refinement Logic

1. Generate CAPTCHA
2. Predict difficulty
3. Adjust noise, distortion, clutter
4. Repeat until target difficulty is achieved

---

## 📸 Screenshots

### Generator UI

*(Add screenshot here)*

### Refinement Mode

*(Add screenshot here)*

---

## 💡 Future Enhancements

* Reinforcement learning-based difficulty tuning
* Human feedback loop integration
* Support for audio CAPTCHAs & image puzzles
* Adversarial bot-resistance testing

---

## 👨‍💻 Author

**Sanyam Katoch**
ML • AI • Computer Vision
[GitHub](https://github.com/sanyam-katoch10)

Do you want me to make that version too?
