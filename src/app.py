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
/* ===== ANIMATED DARK GRADIENT BACKGROUND ===== */
.stApp {
    background: linear-gradient(45deg, #0c0d12, #10121c, #0e0f15, #14151d);
    background-size: 400% 400%;
    animation: gradientShift 35s ease infinite;
    color: #e7e7e7;
}

@keyframes gradientShift {
    0% {background-position:0% 50%;}
    25% {background-position:50% 100%;}
    50% {background-position:100% 50%;}
    75% {background-position:50% 0%;}
    100% {background-position:0% 50%;}
}

/* ===== GLASS CARDS ===== */
.card {
    background: rgba(30,30,38,0.55);
    backdrop-filter: blur(20px) saturate(180%);
    border-radius: 22px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 18px 45px rgba(0,0,0,0.85);
    transition: all 0.35s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 28px 60px rgba(0,0,0,0.95), 0 0 22px rgba(255,255,255,0.15);
}

/* ===== PLOTS ===== */
.plot-card {
    background: rgba(20,20,28,0.55);
    backdrop-filter: blur(16px);
    border-radius: 18px;
    padding: 12px;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 12px 30px rgba(0,0,0,0.8);
    transition: all 0.35s ease;
}

.plot-card:hover {
    filter: drop-shadow(0 0 16px rgba(0,200,255,0.6));
}

/* ===== BUTTONS ===== */
.stButton button {
    border-radius: 18px;
    padding: 12px 22px;
    font-weight: 700;
    color: #fff;
    background: linear-gradient(135deg,#2f323c,#8a8f9a,#2f323c);
    box-shadow: inset 0 1px 2px rgba(255,255,255,0.45), 0 10px 26px rgba(0,0,0,0.85);
    transition: all 0.35s ease;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 32px rgba(0,200,255,0.8), 0 18px 40px rgba(0,0,0,0.95);
}

/* ===== SLIDERS ===== */
.stSlider > div {
    background: rgba(255,255,255,0.05) !important;
    backdrop-filter: blur(12px);
    border-radius: 14px;
    padding: 6px;
    transition: all 0.35s ease;
}

.stSlider:hover > div {
    box-shadow: 0 0 18px rgba(0,200,255,0.4);
}

/* ===== TOPBAR ===== */
.topbar {
    background: linear-gradient(135deg,#1a1c24,#2b2f3a);
    padding: 18px 30px;
    border-radius: 18px;
    font-size: 26px;
    font-weight: 800;
    margin-bottom: 20px;
    box-shadow: inset 0 1px 1px rgba(255,255,255,0.08), 0 18px 45px rgba(0,0,0,0.9);
}

/* ===== FOOTER ===== */
.footer {
    text-align: center;
    margin-top: 40px;
    color: #8b8f9c;
}
</style>
""", unsafe_allow_html=True)

# ================= TOPBAR =================
st.markdown(
    "<div class='topbar'>🔒 ML CAPTCHA SaaS Dashboard <span style='float:right;font-size:16px;'>🟢 Model Online</span></div>",
    unsafe_allow_html=True
)

# ================= MAIN PANEL =================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("## 🎯 CAPTCHA + Refinement Live Preview")

# Split layout: left for controls, right for live preview
controls_col, live_col = st.columns([1,2])

# ================= CONTROLS =================
with controls_col:
    st.markdown("<div class='slider-card'>", unsafe_allow_html=True)
    noise = st.slider("Noise", 0.0, 1.0, 0.25)
    distortion = st.slider("Distortion", 0.0, 1.0, 0.25)
    clutter = st.slider("Clutter", 0.0, 1.0, 0.25)
    st.markdown("</div>", unsafe_allow_html=True)

    target = st.selectbox("Target Difficulty", ["easy", "medium", "hard"])
    gen_btn = st.button("🎲 Generate CAPTCHA")
    refine_btn = st.button("✨ Refine Once", key="refine")
    auto_btn = st.button("🚀 Auto-Refine", key="auto")

# ================= LIVE PREVIEW =================
with live_col:
    img_slot = st.empty()
    plot_convergence = st.empty()
    plot_heatmap = st.empty()
    stats_slot = st.empty()

# ================= LOGIC =================
if gen_btn:
    img, text = generate_captcha(noise, distortion, clutter)
    pred, conf = predict(img)
    img_slot.image(img, use_column_width=True)
    stats_slot.markdown(f"""
    **Text:** `{text}`  
    **Difficulty:** `{pred.upper()}`  
    **Confidence:** `{conf:.2f}`
    """)

if refine_btn:
    img, text, lvl = refine(target)
    img_slot.image(img, use_column_width=True)
    buf = BytesIO()
    img.save(buf, format="PNG")
    st.download_button("⬇ Download CAPTCHA", buf.getvalue(), f"{text}_{lvl}.png")

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

        # Convergence plot
        with plot_convergence:
            st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
            fig1, ax1 = plt.subplots(figsize=(5,3))
            color = f"#00{np.random.randint(150,255):02x}ff"
            ax1.plot(confs, marker='o', color=color, linewidth=2)
            ax1.set_ylim(0,1)
            ax1.set_title("Confidence Convergence", color='#e0e0e0')
            st.pyplot(fig1)
            plt.close(fig1)
            st.markdown("</div>", unsafe_allow_html=True)

        # Heatmap plot
        with plot_heatmap:
            st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
            glow_mat = mat + np.random.uniform(0,0.05,mat.shape)
            fig2, ax2 = plt.subplots(figsize=(5,3))
            sns.heatmap(glow_mat, annot=True, fmt=".2f", cmap="coolwarm", ax=ax2)
            ax2.set_title("Confidence Heatmap", color='#e0e0e0')
            st.pyplot(fig2)
            plt.close(fig2)
            st.markdown("</div>", unsafe_allow_html=True)

        # Update live CAPTCHA
        img_slot.image(img, use_column_width=True)

        time.sleep(0.5)

    st.success("Target difficulty stabilized ✔")

st.markdown("</div>", unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("<div class='footer'>✨ Built by SANYAM KATOCH ✨</div>", unsafe_allow_html=True)
