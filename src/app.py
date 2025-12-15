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

# Animated dark gradient background + subtle streaks
st.markdown("""
<style>
.stApp { background: none; color: #e5e5e5; position: relative; overflow: hidden; }

#animated-bg {
    position: fixed; top:0; left:0; width:100vw; height:100vh;
    background: linear-gradient(135deg, #1c1c1c, #2a2a2a, #3a3a3a, #2e2e2e);
    background-size: 600% 600%;
    animation: bgGradient 40s ease infinite;
    z-index: -100;
}

#light-streaks {
    position: fixed; top: -50%; left: -50%; width: 200%; height: 200%;
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

@keyframes bgGradient { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
@keyframes streakMove { 0% { transform: translate(0%,0%) rotate(0deg); } 100% { transform: translate(50%,50%) rotate(0deg); } }
</style>
<div id="animated-bg"></div>
<div id="light-streaks"></div>
""", unsafe_allow_html=True)

# Existing particles
particle_colors = ["#4facfe", "#00f2fe", "#3a7bd5"]  
for _ in range(25):
    left = random.randint(0, 100)
    delay = random.randint(0, 20)
    color = random.choice(particle_colors)
    st.markdown(f"<div class='particle' style='left:{left}%; animation-delay:{delay}s; background:{color}; box-shadow:0 0 10px {color}'></div>", unsafe_allow_html=True)

# Hero title and subtitle
st.markdown('<h1 class="hero-title">🔐 ML CAPTCHA Refinement</h1>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Self-optimizing CAPTCHA system with real-time ML feedback</div>', unsafe_allow_html=True)

# Three main columns
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

    chart_col1, chart_col2 = st.columns(2)
    line_placeholder = chart_col1.empty()
    heatmap_placeholder = chart_col2.empty()

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

        # Initialize line and heatmap figures
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

            # Update convergence line
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

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<center style='margin-top:40px;color:#9ca3af;'>✨ Made by SANYAM KATOCH ✨</center>", unsafe_allow_html=True)
