import streamlit as st
from io import BytesIO
from generator import generate_captcha
from refine_m import refine, predict
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time
import random

st.set_page_config(page_title="ML CAPTCHA Refinement", page_icon="🔐", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(270deg, #4facfe, #00f2fe, #3a7bd5);
    background-size: 600% 600%;
    animation: animatedGradient 20s ease infinite;
    color: white;
}
@keyframes animatedGradient {
    0% {background-position:0% 50%;}
    50% {background-position:100% 50%;}
    100% {background-position:0% 50%;}
}
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
}
.particle {
    position: fixed;
    width: 6px;
    height: 6px;
    background: rgba(255,255,255,0.5);
    border-radius: 50%;
    animation: float 20s infinite linear;
    z-index: 0;
}
@keyframes float {
    from { transform: translateY(100vh); }
    to { transform: translateY(-10vh); }
}
.glass {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(18px);
    border-radius: 20px;
    padding: 25px;
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}
.hero-title {
    font-size: 50px;
    font-weight: 800;
    text-align: center;
    margin-top: 0px;
}
.hero-sub {
    text-align: center;
    color: #d1d5db;
    margin-bottom: 40px;
    font-size: 18px;
}
.stButton button {
    background: linear-gradient(135deg, #4facfe, #00f2fe);
    border-radius: 14px;
    font-weight: 600;
    border: none;
}
</style>
""", unsafe_allow_html=True)


for _ in range(25):
    left = random.randint(0, 100)
    delay = random.randint(0, 20)
    st.markdown(f"<div class='particle' style='left:{left}%; animation-delay:{delay}s'></div>", unsafe_allow_html=True)

st.markdown('<h1 class="hero-title">🔐 ML CAPTCHA Refinement</h1>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Self-optimizing CAPTCHA system with real-time ML feedback</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1.2, 1.8, 1.4])

with col1:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown("### ⚙️ Manual Controls")
    noise = st.slider("Noise", 0.0, 1.0, 0.2)
    dist = st.slider("Distortion", 0.0, 1.0, 0.2)
    clutter = st.slider("Clutter", 0.0, 1.0, 0.2)
    gen = st.button("🎲 Generate CAPTCHA", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown("### 🖼️ CAPTCHA Preview")
    if gen:
        img, text = generate_captcha(noise, dist, clutter)
        st.image(img, use_column_width=True)
        pred, conf = predict(img)
        st.markdown(f"**Text:** `{text}`  \n**Predicted Difficulty:** `{pred.upper()}`  \n**Confidence:** `{conf:.2f}`")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown("### 🔁 CAPTCHA Refinement")
    target = st.selectbox("Target Difficulty", ["easy", "medium", "hard"])
    refine_btn = st.button("✨ Refine CAPTCHA")
    auto = st.button("🚀 Start Auto-Refinement")
    heatmap_btn = st.button("📊 Show Difficulty Heatmap")
    chart_placeholder = st.empty()

    if refine_btn:
        img, text, predicted = refine(target)
        st.image(img, use_column_width=True)
        buf = BytesIO()
        img.save(buf, format="PNG")
        st.download_button("⬇️ Download CAPTCHA", data=buf.getvalue(), file_name=f"{text}_{predicted}.png", mime="image/png", use_container_width=True)

    if auto:
        confidences = []
        for step in range(6):
            img, text, pred = refine(target)
            _, conf = predict(img)
            confidences.append(conf)
            fig, ax = plt.subplots()
            ax.plot(confidences, marker='o')
            ax.set_ylim(0, 1)
            ax.set_title("Confidence Convergence")
            ax.set_xlabel("Iteration")
            ax.set_ylabel("Confidence")
            chart_placeholder.pyplot(fig)
            time.sleep(0.7)
        st.success("Target difficulty stabilized ✅")

    if heatmap_btn:
        grid_size = 5
        difficulties = np.zeros((grid_size, grid_size))
        for i in range(grid_size):
            for j in range(grid_size):
                img, text = generate_captcha(noise, dist, clutter)
                _, conf = predict(img)
                difficulties[i, j] = conf
        fig, ax = plt.subplots(figsize=(5,5))
        sns.heatmap(difficulties, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        ax.set_title("Difficulty Heatmap")
        st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<center style='margin-top:40px;color:#9ca3af;'>✨ Made by SANYAM KATOCH ✨</center>", unsafe_allow_html=True)
