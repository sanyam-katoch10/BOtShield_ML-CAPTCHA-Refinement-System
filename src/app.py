import streamlit as st
from io import BytesIO
from generator import generate_captcha
from refine_m import refine, predict
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time
import random

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="ML CAPTCHA Refinement",
    page_icon="🔐",
    layout="wide"
)

# -----------------------------
# CSS Styling
# -----------------------------
st.markdown("""
<style>
/* Background Gradient Animation */
.stApp {
    background: linear-gradient(135deg, #0b0c10, #1f2833, #45a29e);
    background-size: 400% 400%;
    animation: gradientFlow 25s ease infinite;
    color: #e0e0e0;
    font-family: 'Segoe UI', sans-serif;
}

@keyframes gradientFlow {
    0% { background-position: 0% 0%; }
    25% { background-position: 50% 50%; }
    50% { background-position: 100% 100%; }
    75% { background-position: 50% 50%; }
    100% { background-position: 0% 0%; }
}

/* Particle Effects */
.particle {
    position: fixed;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    animation: float 20s linear infinite;
    z-index: 0;
    box-shadow: 0 0 8px rgba(255,255,255,0.2);
}
@keyframes float {
    from { transform: translateY(100vh); }
    to { transform: translateY(-10vh); }
}

/* Glassmorphism Panels */
.glass {
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(22px);
    border-radius: 20px;
    padding: 30px;
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 10px 40px rgba(0,0,0,0.6);
}

/* Hero Text */
.hero-title {
    font-size: 52px;
    font-weight: 900;
    text-align: center;
    margin-top: 10px;
    color: #e0e0e0;
}
.hero-sub {
    text-align: center;
    color: #b0b0b0;
    font-size: 18px;
    margin-bottom: 40px;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #1f1c2c, #928dab);
    border-radius: 14px;
    font-weight: 600;
    border: none;
    color: #fff;
    padding: 0.6rem 1.4rem;
    transition: transform 0.2s ease;
}
.stButton>button:hover {
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Particles Animation
# -----------------------------
particle_colors = ["#4facfe", "#00f2fe", "#3a7bd5"]
for _ in range(20):
    left = random.randint(0, 100)
    delay = random.randint(0, 20)
    color = random.choice(particle_colors)
    st.markdown(
        f"<div class='particle' style='left:{left}%; animation-delay:{delay}s; background:{color}; box-shadow:0 0 12px {color}'></div>",
        unsafe_allow_html=True
    )

# -----------------------------
# Hero Section
# -----------------------------
st.markdown('<h1 class="hero-title">🔐 ML CAPTCHA Refinement</h1>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Self-optimizing CAPTCHA system with real-time ML feedback</div>', unsafe_allow_html=True)

# -----------------------------
# Layout Columns
# -----------------------------
col1, col2, col3 = st.columns([1.2, 1.8, 1.4])

# -----------------------------
# Column 1: Manual Controls
# -----------------------------
with col1:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown("### ⚙️ Manual Controls")
    noise = st.slider("Noise", 0.0, 1.0, 0.2)
    dist = st.slider("Distortion", 0.0, 1.0, 0.2)
    clutter = st.slider("Clutter", 0.0, 1.0, 0.2)
    gen = st.button("🎲 Generate CAPTCHA", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Column 2: CAPTCHA Preview
# -----------------------------
with col2:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown("### 🖼️ CAPTCHA Preview")
    if gen:
        img, text = generate_captcha(noise, dist, clutter)
        st.image(img, use_column_width=True)
        pred, conf = predict(img)
        st.markdown(f"**Text:** `{text}`  \n**Predicted Difficulty:** `{pred.upper()}`  \n**Confidence:** `{conf:.2f}`")
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Column 3: CAPTCHA Refinement
# -----------------------------
with col3:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown("### 🔁 CAPTCHA Refinement")
    target = st.selectbox("Target Difficulty", ["easy", "medium", "hard"])
    refine_btn = st.button("✨ Refine CAPTCHA")
    auto = st.button("🚀 Start Auto-Refinement")
    line_placeholder = st.empty()
    heatmap_placeholder = st.empty()

    if refine_btn:
        img, text, predicted = refine(target)
        st.image(img, use_column_width=True)

    if auto:
        grid_size = 5
        confidences = []
        difficulties = np.zeros((grid_size, grid_size))
        for step in range(6):
            for i in range(grid_size):
                for j in range(grid_size):
                    img, text, pred = refine(target)
                    _, conf = predict(img)
                    difficulties[i, j] = conf

            avg_conf = difficulties.mean()
            confidences.append(avg_conf)
            fig_line, ax_line = plt.subplots()
            ax_line.plot(confidences, marker='o', color="#00ffff", linewidth=2)
            ax_line.set_ylim(0, 1)
            ax_line.set_facecolor("#0f1a25")
            ax_line.set_title("Average Confidence Convergence", color="#e5e5e5")
            ax_line.set_xlabel("Iteration", color="#c0c0c0")
            ax_line.set_ylabel("Confidence", color="#c0c0c0")
            ax_line.tick_params(colors="#c0c0c0")
            line_placeholder.pyplot(fig_line)

            fig_heat, ax_heat = plt.subplots(figsize=(5,5))
            sns.heatmap(difficulties, annot=True, fmt=".2f", cmap="coolwarm", ax=ax_heat, cbar_kws={'color':'#e5e5e5'})
            ax_heat.set_title(f"Difficulty Heatmap (Step {step+1})", color="#e5e5e5")
            ax_heat.tick_params(colors="#c0c0c0")
            heatmap_placeholder.pyplot(fig_heat)

            time.sleep(0.7)
        st.success("Target difficulty stabilized ✅")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<center style='margin-top:40px;color:#9ca3af;'>✨ Made by SANYAM KATOCH ✨</center>", unsafe_allow_html=True)
