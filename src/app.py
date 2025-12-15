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
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    background-size: 400% 400%;
    animation: gradientFlow 25s ease infinite;
    color: #e5e5e5;
}
@keyframes gradientFlow {
    0% { background-position: 0% 0%; }
    25% { background-position: 50% 50%; }
    50% { background-position: 100% 100%; }
    75% { background-position: 50% 50%; }
    100% { background-position: 0% 0%; }
}
.block-container {
    padding-top: 0rem;
    padding-bottom: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
}
.particle {
    position: fixed;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    animation: float 20s infinite linear;
    z-index: 0;
    box-shadow: 0 0 8px rgba(255,255,255,0.15);
}
@keyframes float {
    from { transform: translateY(100vh); }
    to { transform: translateY(-10vh); }
}
.glass {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(18px);
    border-radius: 20px;
    padding: 25px;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 8px 32px rgba(0,0,0,0.6);
}
.hero-title {
    font-size: 50px;
    font-weight: 800;
    text-align: center;
    margin-top: 0px;
    color: #e5e5e5;
}
.hero-sub {
    text-align: center;
    color: #c0c0c0;
    margin-bottom: 40px;
    font-size: 18px;
}
.stButton button {
    background: linear-gradient(135deg, #1f1c2c, #928dab);
    border-radius: 14px;
    font-weight: 600;
    border: none;
    color: #fff;
}
</style>
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
    confidences = []
    difficulties = np.zeros((grid_size, grid_size))

    # Initialize empty figures for live update
    fig_line, ax_line = plt.subplots(figsize=(7,5))
    ax_line.set_ylim(0,1)
    ax_line.set_facecolor("white")
    fig_line.patch.set_facecolor("white")
    ax_line.set_title("Average Confidence Convergence", color="black")
    ax_line.set_xlabel("Iteration", color="black")
    ax_line.set_ylabel("Confidence", color="black")
    ax_line.tick_params(colors="black")
    line_plot, = ax_line.plot([], [], marker='o', color='green', linewidth=2)
    line_placeholder.pyplot(fig_line, clear_figure=True)

    fig_heat, ax_heat = plt.subplots(figsize=(7,5))
    heatmap_placeholder.pyplot(fig_heat, clear_figure=True)

    for step in range(6):
        for i in range(grid_size):
            for j in range(grid_size):
                img, text, pred = refine(target)
                _, conf = predict(img)
                difficulties[i, j] = conf

        avg_conf = difficulties.mean()
        confidences.append(avg_conf)

        # Update convergence line smoothly
        line_plot.set_data(range(len(confidences)), confidences)
        ax_line.set_xlim(0, max(5,len(confidences)))
        line_placeholder.pyplot(fig_line, clear_figure=True)

        # Update heatmap
        ax_heat.clear()
        hm = sns.heatmap(difficulties, annot=True, fmt=".2f", cmap="coolwarm", square=True, ax=ax_heat)
        cbar = hm.collections[0].colorbar
        cbar.ax.tick_params(color="black", labelcolor="black")
        ax_heat.tick_params(colors="black")
        fig_heat.patch.set_facecolor("white")
        heatmap_placeholder.pyplot(fig_heat, clear_figure=True)

        time.sleep(0.5)

    st.success("Target difficulty stabilized ✅")

st.markdown("<center style='margin-top:40px;color:#9ca3af;'>✨ Made by SANYAM KATOCH ✨</center>", unsafe_allow_html=True)
