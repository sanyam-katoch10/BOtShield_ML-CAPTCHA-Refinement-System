import streamlit as st
from io import BytesIO
from generator import generate_captcha
from refine_m import refine, predict
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time

# ================= CONFIG =================
st.set_page_config(
    page_title="ML CAPTCHA SaaS Dashboard",
    page_icon="🔒",
    layout="wide"
)

# ================= CSS =================
st.markdown("""
<style>
/* ===== ANIMATED DARK BACKGROUND ===== */
.stApp {
    background: linear-gradient(120deg, #0a0a0a, #1b1b1b, #0f0f0f);
    background-size: 300% 300%;
    animation: bgShift 25s ease infinite;
    color: #eaeaea;
}

@keyframes bgShift {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* ===== GLASS CARDS ===== */
.card, .plot-card {
    background: rgba(30,30,38,0.55);
    backdrop-filter: blur(18px) saturate(180%);
    border-radius: 22px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 18px 45px rgba(0,0,0,0.85);
    transition: all 0.35s ease;
}

.card:hover, .plot-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 28px 60px rgba(0,0,0,0.95), 0 0 20px rgba(255,255,255,0.12);
}

/* ===== BUTTONS ===== */
.stButton button {
    border-radius: 16px;
    border: none;
    padding: 14px;
    font-weight: 700;
    color: #fff;
    background: linear-gradient(135deg,#3b3b3b,#9b9b9b,#3b3b3b);
    box-shadow: inset 0 1px 1px rgba(255,255,255,0.4),
                0 6px 18px rgba(0,0,0,0.7);
    transition: all 0.3s ease;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 20px rgba(220,220,220,0.35),
                0 10px 30px rgba(0,0,0,0.9);
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#101010,#1c1c1c);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* ===== FOOTER ===== */
.footer {
    text-align: center;
    margin-top: 40px;
    color: #8d8d8d;
}
</style>
""", unsafe_allow_html=True)

# ================= TOPBAR =================
st.markdown(
    "<div class='card' style='text-align:center;font-size:26px;font-weight:800;'>🔒 ML CAPTCHA Refinement 🔹 Model Online</div>",
    unsafe_allow_html=True
)

# ================= LAYOUT =================
gen_col, refine_col = st.columns([1,2])

# ================= GENERATOR =================
with gen_col:
    st.markdown("<div class='card'><h3>🖼 CAPTCHA Generator</h3></div>", unsafe_allow_html=True)
    noise = st.slider("Noise", 0.0,1.0,0.25)
    distortion = st.slider("Distortion", 0.0,1.0,0.25)
    clutter = st.slider("Clutter", 0.0,1.0,0.25)
    gen_btn = st.button("🎲 Generate CAPTCHA")
    img_slot = st.empty()
    stats_slot = st.empty()

    if gen_btn:
        img, text = generate_captcha(noise, distortion, clutter)
        pred, conf = predict(img)
        img_slot.image(img, use_column_width=True)
        stats_slot.markdown(f"**Text:** `{text}`  \n**Difficulty:** `{pred.upper()}`  \n**Confidence:** `{conf:.2f}`")

# ================= REFINEMENT ENGINE =================
with refine_col:
    st.markdown("<div class='card'><h3>🔁 Refinement Engine</h3></div>", unsafe_allow_html=True)
    target = st.selectbox("Target Difficulty", ["easy","medium","hard"])
    refine_btn = st.button("✨ Refine Once", key="refine")
    auto_btn = st.button("🚀 Auto-Refine", key="auto")

    img_slot_refine = st.empty()
    plot_col1, plot_col2 = st.columns(2)
    buf_slot = st.empty()

# ================= SINGLE LIVE REFINEMENT =================
if refine_btn:
    img, text, lvl = refine(target)
    img_slot_refine.image(img, use_column_width=True)
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf_slot.download_button("⬇ Download CAPTCHA", buf.getvalue(), f"{text}_{lvl}.png")

if auto_btn:
    confs = []
    for step in range(6):
        mat = np.zeros((4,4))
        for i in range(4):
            for j in range(4):
                img, _, _ = refine(target)
                _, c = predict(img)
                mat[i,j] = c

        confs.append(mat.mean())
        img_slot_refine.image(img, use_column_width=True)

        # CONVERGENCE LINE (ONLY ONE)
        with plot_col1:
            st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
            fig1, ax1 = plt.subplots(figsize=(4,3))
            ax1.plot(confs, marker='o', color='#00ffff', linewidth=2)
            ax1.set_ylim(0,1)
            ax1.set_title("Convergence", color='white')
            st.pyplot(fig1)
            plt.close(fig1)
            st.markdown("</div>", unsafe_allow_html=True)

        # HEATMAP (ONLY ONE)
        with plot_col2:
            st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
            fig2, ax2 = plt.subplots(figsize=(4,3))
            sns.heatmap(mat, annot=True, fmt=".2f", cmap="coolwarm", ax=ax2)
            ax2.set_title("Confidence Heatmap", color='white')
            st.pyplot(fig2)
            plt.close(fig2)
            st.markdown("</div>", unsafe_allow_html=True)

        time.sleep(0.5)

    st.success("Target difficulty stabilized ✔")

# ================= FOOTER =================
st.markdown("<div class='footer'>✨ Built by SANYAM KATOCH ✨</div>", unsafe_allow_html=True)
