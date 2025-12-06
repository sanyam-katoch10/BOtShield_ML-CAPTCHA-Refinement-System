

<p align="center">
  <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" width="80"/>
</p>
<h1 align="center">ML-Enhanced CAPTCHA Refinement System</h1>
<h3 align="center">AI-Powered Adaptive CAPTCHA Generator & Difficulty Classifier</h3>


<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/TensorFlow-Keras-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Streamlit-Live_App-ff4b4b?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/OpenCV-Image Processing-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge"/>
</p>

---

# 🌐 **Live Demo**

<p align="center">
  🔗 **Coming Soon** — Your Streamlit App URL will go here  
</p>

---

# 🎯 **Project Summary**

The **ML-Enhanced CAPTCHA Refinement System** intelligently generates CAPTCHAs and automatically adjusts their difficulty using a **CNN classifier**.
This ensures the perfect balance between:

✔️ **Human readability**
✔️ **Bot resistance**
✔️ **Security + Usability**

The system dynamically modulates **noise**, **distortion**, and **clutter** until the generated CAPTCHA matches the desired difficulty level:
**Easy**, **Medium**, or **Hard**.

---

# ✨ **Features**

### 🔐 **Smart CAPTCHA Generator**

* Adjustable noise, distortion, and clutter
* Dynamic random text generation
* Fully image-based CAPTCHA pipeline

### 🤖 **CNN Difficulty Classifier**

* Trained on 6,000 synthetic images
* 95% classification accuracy
* TensorFlow/Keras-based

### 🔄 **Adaptive Refinement Loop**

* Predict → Adjust → Re-generate → Repeat
* Ensures output matches target difficulty
* Efficient for real-time apps

### 🎨 **Beautiful Streamlit UI**

* Dark-themed interface
* Sliders + live prediction
* Instant download button
* Smooth and responsive UX

---

# 🧠 **Architecture Diagram**

```
CAPTCHA Generation → CNN Classifier → Difficulty Check → Adjust Distortion/Noise/Clutter → OUTPUT
```

---

# 📁 **Project Structure**

```
ML-CAPTCHA-Refinement/
│
├── src/
│   ├── generator.py        # CAPTCHA generation script
│   ├── refine_m.py         # Difficulty refinement loop
│   ├── train_model.py      # Training script for CNN
│   ├── app.py              # Streamlit web app
│
├── models/
│   └── captcha_model.keras # Trained ML model (Large file)
│
├── requirements.txt
└── README.md
```

---

# 🛠️ **Tech Stack**

| Component         | Technology                       |
| ----------------- | -------------------------------- |
| Frontend UI       | Streamlit                        |
| ML Framework      | TensorFlow / Keras               |
| Image Processing  | OpenCV, Pillow                   |
| CAPTCHA Generator | `captcha` library                |
| Deployment        | Streamlit Cloud                  |
| Dataset Creation  | Python-based synthetic generator |

---

# 🚀 **Installation**

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/ML-CAPTCHA-Refinement.git
cd ML-CAPTCHA-Refinement
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run Streamlit App

```bash
streamlit run src/app.py
```

---

# 🧪 **Machine Learning Details**

### 📌 Model

A lightweight **Convolutional Neural Network** trained on synthetic CAPTCHA images.

### 📌 Training Summary

* 6,000 labeled images (easy/medium/hard)
* 95% accuracy on test set
* Conv2D + MaxPooling layers
* Dropout for regularization
* Adam optimizer
* Categorical Cross-Entropy loss

### 📌 Refinement Logic

1. Generate CAPTCHA
2. Predict difficulty
3. Adjust settings
4. Repeat until target difficulty is achieved

---

# 📸 **Screenshots**

### 🖼️ Generator UI

(Add your screenshot)

### 🔄 Refinement Mode

(Add your screenshot)

---


# 💡 **Future Enhancements**

* Reinforcement learning-based difficulty tuning
* Human feedback loop integration
* Support for audio & image puzzles
* Adversarial bot-resistance testing

---

# 👨‍💻 **Author**

**Sanyam Katoch**
📌 ML • AI • Computer Vision
🔗 GitHub: *add your link here*

