import streamlit as st
from io import BytesIO
from generator import generate_captcha
from refine_m import refine, predict
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import time

st.set_page_config(page_title="ML CAPTCHA Refinement", page_icon="🔒", layout="wide")

if "conf_history" not in st.session_state:
    st.session_state.conf_history = []

def update_avg_conf(c):
    st.session_state.conf_history.append(c)
    return float(np.mean(st.session_state.conf_history))

def get_avg_conf():
    return float(np.mean(st.session_state.conf_history)) if st.session_state.conf_history else 0.0

st.markdown("""
<style>
.stApp {
    font-family: 'Segoe UI', sans-serif;
    overflow: hidden;
    color: #eaeaea;
    background: linear-gradient(-45deg, #1b1b1b, #2a2a2a, #121212, #2e2e2e);
    background-size: 1000% 1000%;
    animation: gradientShift 30s ease infinite;
}
@keyframes gradientShift {
    0% {background-position:0% 50%;}
    50% {background-position:100% 50%;}
    100% {background-position:0% 50%;}
}
.topbar {
    background: rgba(30,30,30,0.7);
    backdrop-filter: blur(16px);
    padding: 20px 30px;
    border-radius: 20px;
    box-shadow: 0 0 20px #00ffff, 0 0 30px #ff00ff;
    margin-bottom: 25px;
    font-size: 28px;
    font-weight: 800;
}
section[data-testid="stSidebar"] {
    background: rgba(20,20,20,0.85);
    backdrop-filter: blur(12px);
}
.card {
    background: rgba(40,40,40,0.45);
    backdrop-filter: blur(15px);
    border-radius: 20px;
    padding: 25px;
    border: 2px solid #00ffff;
    box-shadow: 0 0 25px rgba(0,255,255,0.3),
                0 0 35px rgba(255,0,255,0.3);
}
.stButton button {
    border-radius: 16px;
    font-weight: 700;
    color: #fff;
    background: linear-gradient(135deg,#3b3b3b,#7b7b7b,#3b3b3b);
}
.footer {
    text-align:center;
    margin-top:40px;
    color:#8d8d8d;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='topbar'>🔒 ML CAPTCHA Refinement <span style='float:right;font-size:16px;'>🟢 Model Online</span></div>", unsafe_allow_html=True)

with st.sidebar:
    page = st.radio("", ["📊 Dashboard", "🖼 CAPTCHA Generator", "🔁 Refinement Engine"])

if page == "📊 Dashboard":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='card'>### Live Avg Confidence<br><h2>{get_avg_conf():.2f}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card'>### Stability Status<br><h2>Stable</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='card'>### Active Model<br><h2>CNN v1.0</h2></div>", unsafe_allow_html=True)

elif page == "🖼 CAPTCHA Generator":
    col1, col2 = st.columns([1.2, 1.8])
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        noise = st.slider("Noise", 0.0, 1.0, 0.25)
        distortion = st.slider("Distortion", 0.0, 1.0, 0.25)
        clutter = st.slider("Clutter", 0.0, 1.0, 0.25)
        gen = st.button("🎲 Generate CAPTCHA")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        slot = st.empty()
        if gen:
            img, text = generate_captcha(noise, distortion, clutter)
            slot.image(img, use_column_width=True)
            pred, conf = predict(img)
            avg = update_avg_conf(conf)
            st.markdown(f"**Text:** `{text}`  \n**Difficulty:** `{pred.upper()}`  \n**Confidence:** `{conf:.2f}`  \n**Live Avg Confidence:** `{avg:.2f}`")
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "🔁 Refinement Engine":
    target = st.selectbox("Target Difficulty", ["easy", "medium", "hard"])
    refine_btn = st.button("✨ Refine Once")
    auto_btn = st.button("🚀 Auto-Refine")

    live_slot = st.empty()
    avg_slot = st.empty()

    col1, col2 = st.columns(2)
    conv_slot = col1.empty()
    heat_slot = col2.empty()

    if refine_btn:
        img, text, lvl = refine(target)
        live_slot.image(img, use_column_width=True)
        _, c = predict(img)
        avg = update_avg_conf(c)
        avg_slot.markdown(f"<div class='card'>### Live Avg Confidence<br><h2>{avg:.2f}</h2></div>", unsafe_allow_html=True)
        buf = BytesIO()
        img.save(buf, format="PNG")
        st.download_button("⬇ Download CAPTCHA", buf.getvalue(), f"{text}_{lvl}.png")

    if auto_btn:
        confs = []
        grid = 4
        mat_current = np.zeros((grid, grid))
        norm = mcolors.Normalize(vmin=0, vmax=1)
        cmap = plt.cm.plasma

        for step in range(6):
            mat_target = np.zeros((grid, grid))
            for i in range(grid):
                for j in range(grid):
                    img, _, _ = refine(target)
                    live_slot.image(img, use_column_width=True)
                    _, c = predict(img)
                    mat_target[i, j] = c
                    avg = update_avg_conf(c)
                    avg_slot.markdown(f"<div class='card'>### Live Avg Confidence<br><h2>{avg:.2f}</h2></div>", unsafe_allow_html=True)
            confs.append(mat_target.mean())

            for t in range(20):
                interp = mat_current + (mat_target - mat_current) * ((t + 1) / 20)
                fig1, ax1 = plt.subplots()
                ax1.plot(confs)
                ax1.set_ylim(0, 1)
                conv_slot.pyplot(fig1, clear_figure=True)
                plt.close(fig1)

                fig2, ax2 = plt.subplots()
                ax2.imshow(interp, cmap=cmap, norm=norm)
                heat_slot.pyplot(fig2, clear_figure=True)
                plt.close(fig2)
                time.sleep(0.05)

            mat_current = mat_target.copy()

        st.success("Target difficulty stabilized ✔")

st.markdown("<div class='footer'>✨ Built by SANYAM KATOCH ✨</div>", unsafe_allow_html=True)
