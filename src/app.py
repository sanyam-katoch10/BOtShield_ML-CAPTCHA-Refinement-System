import streamlit as st
from io import BytesIO
from generator import generate_captcha
from refine_m import refine, predict
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time

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
    box-shadow: 0 0 12px rgba(255,255,255,0.25);
    opacity: 0.7;
}

.particle:nth-child(2) { width: 8px; height: 8px; animation-duration: 25s; }
.particle:nth-child(3) { width: 5px; height: 5px; animation-duration: 15s; }
.particle:nth-child(4) { width: 10px; height: 10px; animation-duration: 30s; }

@keyframes float {
    0% { transform: translateY(100vh) translateX(0) scale(0.8); opacity:0.5; }
    50% { transform: translateY(50vh) translateX(20px) scale(1.1); opacity:1; }
    100% { transform: translateY(-10vh) translateX(-10px) scale(0.9); opacity:0.5; }
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
    position: relative;
}

.hero-title::after {
    content: '';
    position: absolute;
    left: 50%;
    top: 50%;
    width: 200px;
    height: 60px;
    background: radial-gradient(circle, rgba(255,255,255,0.15), transparent);
    transform: translate(-50%, -50%) scale(1);
    border-radius: 50%;
    animation: pulse 3s infinite ease-in-out;
    z-index: -1;
}

@keyframes pulse {
    0% { transform: translate(-50%, -50%) scale(1); opacity:0.4; }
    50% { transform: translate(-50%, -50%) scale(1.3); opacity:0.7; }
    100% { transform: translate(-50%, -50%) scale(1); opacity:0.4; }
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
    transition: all 0.3s ease;
}

.stButton button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px rgba(255,255,255,0.3);
}
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="banner"><div></div><div></div><div></div></div>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">🔐 ML CAPTCHA Refinement</h1>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Self-optimizing CAPTCHA system with real-time ML feedback</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1.2,1.8,1.4])

with col1:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown("### ⚙️ Manual Controls")
    noise = st.slider("Noise",0.0,1.0,0.2)
    dist = st.slider("Distortion",0.0,1.0,0.2)
    clutter = st.slider("Clutter",0.0,1.0,0.2)
    gen = st.button("🎲 Generate CAPTCHA", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown("### 🖼️ CAPTCHA Preview")
    if gen:
        img,text = generate_captcha(noise,dist,clutter)
        st.image(img,use_column_width=True)
        pred,conf = predict(img)
        st.markdown(f"**Text:** `{text}`  \n**Predicted Difficulty:** `{pred.upper()}`  \n**Confidence:** `{conf:.2f}`")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown("### 🔁 CAPTCHA Refinement")
    target = st.selectbox("Target Difficulty",["easy","medium","hard"])
    refine_btn = st.button("✨ Refine CAPTCHA")
    start_refinement = st.button("🚀 Start Auto-Refinement")

    chart_col1, chart_col2 = st.columns(2)
    line_placeholder = chart_col1.empty()
    heatmap_placeholder = chart_col2.empty()

    if refine_btn:
        img,text,predicted = refine(target)
        st.image(img,use_column_width=True)
        buf=BytesIO()
        img.save(buf,format="PNG")
        st.download_button("⬇️ Download CAPTCHA",data=buf.getvalue(),file_name=f"{text}_{predicted}.png",mime="image/png",use_container_width=True)

    if start_refinement:
        grid_size = 4
        confidences = []
        difficulties = np.zeros((grid_size,grid_size))
        for step in range(6):
            for i in range(grid_size):
                for j in range(grid_size):
                    img, text, predicted = refine(target)
                    _, conf = predict(img)
                    difficulties[i,j] = conf

            confidences.append(difficulties.mean())

            fig_line, ax_line = plt.subplots(figsize=(7, 5))
            ax_line.plot(confidences, marker='o', color="green", linewidth=2)
            ax_line.set_ylim(0, 1)
            ax_line.set_facecolor("white")
            fig_line.patch.set_facecolor("white")
            ax_line.set_title("Average Confidence Convergence", color="black")
            ax_line.set_xlabel("Iteration", color="black")
            ax_line.set_ylabel("Confidence", color="black")
            ax_line.tick_params(colors="black")
            line_placeholder.pyplot(fig_line, clear_figure=True)
            plt.close(fig_line)

            fig_heat, ax_heat = plt.subplots(figsize=(7, 5))
            hm = sns.heatmap(difficulties, annot=True, fmt=".2f", cmap="coolwarm", ax=ax_heat, square=True)
            cbar = hm.collections[0].colorbar
            cbar.ax.tick_params(color="black", labelcolor="black")
            ax_heat.tick_params(colors="black")
            fig_heat.patch.set_facecolor("white")
            heatmap_placeholder.pyplot(fig_heat, clear_figure=True)
            plt.close(fig_heat)

            time.sleep(0.5)
        st.success("Target difficulty stabilized ✅")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<center style='margin-top:40px;color:#9ca3af;'>✨ Made by SANYAM KATOCH ✨</center>", unsafe_allow_html=True)

