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
html, body {
    height: 100%;
    margin: 0;
    padding: 0;
}

/* Remove default Streamlit background */
.stApp {
    background: none;
    color: #e5e5e5;
    position: relative;
    overflow: hidden;
}

/* Dark matte animated gradient background */
#animated-bg {
    position: fixed;
    top:0;
    left:0;
    width:100vw;
    height:100vh;
    background: linear-gradient(135deg, #1c1c1c, #2a2a2a, #3a3a3a, #2e2e2e);
    background-size: 600% 600%;
    animation: bgGradient 40s ease infinite;
    z-index: -100;
}

/* Moving subtle diagonal light streaks */
#light-streaks {
    position: fixed;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: repeating-linear-gradient(
        45deg,
        rgba(255,255,255,0.02) 0px,
        rgba(255,255,255,0.02) 2px,
        transparent 2px,
        transparent 8px
    );
    animation: streakMove 30s linear infinite;
    z-index: -99;
}

@keyframes bgGradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes streakMove {
    0% { transform: translate(0%,0%) rotate(0deg); }
    100% { transform: translate(50%,50%) rotate(0deg); }
}
</style>

<div id="animated-bg"></div>
<div id="light-streaks"></div>
""", unsafe_allow_html=True)



particle_colors = ["#4facfe", "#00f2fe", "#3a7bd5"]  
for _ in range(25):
    left = random.randint(0, 100)
    delay = random.randint(0, 20)
    color = random.choice(particle_colors)
    st.markdown(f"<div class='particle' style='left:{left}%; animation-delay:{delay}s; background:{color}; box-shadow:0 0 10px {color}'></div>", unsafe_allow_html=True)

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
    heatmap_placeholder = st.empty()
    chart_placeholder = st.empty()

    if refine_btn:
        img, text, predicted = refine(target)
        st.image(img, use_column_width=True)
        buf = BytesIO()
        img.save(buf, format="PNG")
        st.download_button("⬇️ Download CAPTCHA", data=buf.getvalue(), file_name=f"{text}_{predicted}.png", mime="image/png", use_container_width=True)

    if auto:
        grid_size = 5
        difficulties = np.zeros((grid_size, grid_size))
        for step in range(6):
            for i in range(grid_size):
                for j in range(grid_size):
                    img, text, pred = refine(target)
                    _, conf = predict(img)
                    difficulties[i, j] = conf

            fig, ax = plt.subplots(figsize=(5,5))
            sns.heatmap(difficulties, annot=True, fmt=".2f", cmap="mako", ax=ax)
            ax.set_title(f"Difficulty Heatmap (Step {step+1})", color="#e5e5e5")
            heatmap_placeholder.pyplot(fig)
            time.sleep(0.7)
        st.success("Target difficulty stabilized ✅")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<center style='margin-top:40px;color:#9ca3af;'>✨ Dark ML Visualization Dashboard ✨</center>", unsafe_allow_html=True)


