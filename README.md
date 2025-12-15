

<p align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdWhhdjd1eXQ5N2d4aWU5MjB1Mmw0OHpiNTR2NjZybHBsc2J0djhmNCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/o0vwzuFwCGAFO/giphy.gif" width="70%" alt="App Demo Animation"/>
</p>

<div align="center">
  <img 
    <img src="pics/s.png" width="150"/
  />
</div>


<h1 align="center">
  <span style="background: linear-gradient(90deg, #ff7eb3, #ff758c, #ff6a88, #ff99ac); -webkit-background-clip: text; color: transparent;">
    🤖 ML-Enhanced CAPTCHA Refinement System 🔐
  </span>
</h1>

<h3 align="center">AI-powered Adaptive CAPTCHA Generator & Difficulty Optimization System</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/TensorFlow-Keras-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-Web_App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/OpenCV-Image_Processing-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white"/>
  <img src="https://img.shields.io/badge/Status-Active-4CAF50?style=for-the-badge"/>
</p>

---

## 🌐 Live Demo

<p align="center">
  <a href="https://sam-ml-captcha-refinement.streamlit.app/" target="_blank">
    <img src="https://img.shields.io/badge/🚀_Launch_Streamlit_App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  </a>
</p>

---

## 🎯 Project Overview

The **ML-Enhanced CAPTCHA Refinement System** intelligently generates, classifies, and adjusts CAPTCHA difficulty levels using a hybrid of:

* Computer Vision
* Deep Learning
* Real-time adaptive feedback
* Streamlit interactive UI

It is designed to balance **human accessibility** with **maximum bot resistance** by dynamically fine-tuning CAPTCHA complexity using a CNN classifier.

<p align="center">
  <img src="https://img.shields.io/badge/Dataset_Size-6000_images-blueviolet?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Model_Accuracy-95%25-brightgreen?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Model_Size-75_MB-orange?style=for-the-badge"/>
</p>

---

### 📊 Classification Report

| Class  | Precision | Recall | F1-Score | Support |
| ------ | --------- | ------ | -------- | ------- |
| easy   | 1.00      | 1.00   | 1.00     | 2000    |
| medium | 1.00      | 0.99   | 0.99     | 2000    |
| hard   | 0.99      | 1.00   | 1.00     | 2000    |

---

## ✨ Key Capabilities

### 🔐 Smart CAPTCHA Generator

* Adjustable **noise**, **distortion**, **clutter**
* Fully randomized CAPTCHA text
* Strong visual variations for training

### 🤖 CNN Difficulty Classifier

* 6000 labeled images (easy/medium/hard)
* 95% validation accuracy
* Lightweight CNN (TensorFlow + Keras)

### 🔄 Adaptive Refinement Loop

* Predict → Adjust → Re-generate → Finalize
* Ensures target difficulty is achieved
* Ideal for **real-time security** use cases

### 🎨 Streamlit Interface

* Dark mode, gradient UI, live preview
* Adjustable sliders
* Instant CAPTCHA download

---

## 🧠 System Architecture

```mermaid
flowchart LR
A([CAPTCHA Generator]) --> B([CNN Difficulty Classifier])
B -->|Check Difficulty| C([Decision Engine])
C -->|Too Easy| D([Increase Noise/Distortion])
C -->|Too Hard| E([Reduce Complexity])
D --> A
E --> A
C --> F([Optimized CAPTCHA Output])
```

---

## 📁 Project Structure

```
ML-CAPTCHA-Refinement/
│
├── src/
│   ├── generator.py        # CAPTCHA generation logic
│   ├── refine_m.py         # Difficulty refinement loop
│   ├── train_model.py      # CNN model training
│   ├── app.py              # Streamlit web app
│
├── models/
│   └── captcha_model.keras # Trained CNN model
│
├── data_preprocessed/      # Preprocessed CAPTCHA dataset
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 🔧 Step 1 — Clone Repository

```bash
git clone https://github.com/your-username/ML-CAPTCHA-Refinement.git
cd ML-CAPTCHA-Refinement
```

### 🧰 Step 2 — Create Virtual Environment

```bash
py -3.11 -m venv venv
venv\Scripts\activate
```

### 📦 Step 3 — Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 🚀 Step 4 — Launch App

```bash
streamlit run src/app.py
```

---

## 🧪 Machine Learning Deep Dive

### 🖼 Dataset

* 6000 images
* 3 difficulty levels:

  * Easy (clean)
  * Medium (moderate noise)
  * Hard (heavy distortion)

### 🧠 CNN Model

* Conv2D → ReLU → MaxPooling
* Dense Layer → Softmax classifier
* Adam optimizer, Categorical Crossentropy

### 🔄 Refinement Algorithm

1. Generate CAPTCHA
2. Predict difficulty
3. Adjust noise/distortion
4. Iterate until target difficulty achieved

---

## 📸 Screenshots

| CAPTCHA Generator                     | Refinement Loop                       | Confusion Matrix                                   |
| ------------------------------------- | ------------------------------------- | -------------------------------------------------- |
| <img src="pics/gen.png" width="600"/> | <img src="pics/ref.png" width="600"/> | <img src="pics/confusion_matrix.png" width="600"/> |

---

## 🚀 Future Enhancements

* Audio CAPTCHA support
* Reinforcement Learning optimization
* Human feedback reinforcement
* Adversarial bot testing

---

## 👤 Developed by

<div align="center">
  <h3>Sanyam Katoch</h3>
  <p>Connect with me:</p>
  
  <p>
    <a href="https://github.com/sanyam-katoch10" target="_blank">
      <img src="https://img.shields.io/badge/GitHub-sanyam--katoch10-000?style=for-the-badge&logo=github" alt="GitHub"/>
    </a>
  </p>
  
  <p>
    <a href="https://www.linkedin.com/in/sanyam-katoch/" target="_blank">
      <img src="https://img.shields.io/badge/LinkedIn-Sanyam--Katoch-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/>
    </a>
  </p>
</div>



