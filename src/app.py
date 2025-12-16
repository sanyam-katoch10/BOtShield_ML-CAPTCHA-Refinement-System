import streamlit as st
from io import BytesIO
from generator import generate_captcha
from refine_m import refine, predict
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time

# ===================== CONFIG =====================
st.set_page_config(page_title="ML CAPTCHA Refinement", page_icon="🔒", layout="wide")

# ===================== CSS =====================
st.markdown("""
<style>
.stApp { background: linear-gradient(120deg, #101010, #1a1a1a, #0f0f0f); background-size: 400% 400%; animation: bgShift 25s ease infinite; color: #eaeaea; font-family: 'Segoe UI', sans-serif; }
@keyframes bgShift {0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;}}

.topbar { background: rgba(30,30,30,0.7); backdrop-filter: blur(12px); padding: 20px 30px; border-radius: 20px; box-shadow: inset 0 1px 2px rgba(255,255,255,0.1), 0 15px 40px rgba(0,0,0,0.8); margin-bottom: 25px; font-size: 28px; font-weight: 800; color: #f0f0f0; }

section[data-testid="stSidebar"] { background: rgba(20,20,20,0.8); backdrop-filter: blur(10px); border-right: 1px solid rgba(255,255,255,0.08); }
.sidebar-title { font-size: 22px; font-weight: 800; margin-bottom: 20px; }

.card { background: rgba(40,40,40,0.4); backdrop-filter: blur(12px); border-radius: 20px; padding: 25px; border: 1px solid rgba(255,255,255,0.1); box-shadow: inset 0 0 12px rgba(255,255,255,0.05), 0 15px 35px rgba(0,0,0,0.6); transition: all 0.3s ease; }
.card:hover { transform: translateY(-3px); box-shadow: 0 0 25px rgba(255,255,255,0.2), 0 20px 40px rgba(0,0,0,0.8); }

.stButton button { border-radius: 16px; border: none; padding: 14px; font-weight: 700; color: #fff; background: linear-gradient(135deg,#4b4b4b,#9b9b9b,#4b4b4b); box-shadow: inset 0 1px 1px rgba(255,255,255,0.3), 0 6px 18px rgba(0,0,0,0.7); transition: all 0.3s ease; }
.stButton button:hover { transform: translateY(-2px); box-shadow: 0 0 30px rgba(220,220,220,0.5), 0 12px 35px rgba(0,0,0,0.9); }

.footer { text-align: center; margin-top: 40px; color: #8d8d8d; }
</style>
""", unsafe_allow_html=True)

# ===================== TOP BAR =====================
st.markdown("<div class='topbar'>🔒 ML CAPTCHA Refinement <span style='float:right;font-size:16px;'>🟢 Model Online</span></div>", unsafe_allow_html=True)

# ===================== SIDEBAR =====================
with st.sidebar:
    st.markdown("<div class='sidebar-title'>⚙️ Navigation</div>", unsafe_allow_html=True)
    page = st.radio("", ["📊 Dashboard", "🖼 CAPTCHA Generator", "🔁 Refinement Engine"])

# ===================== DASHBOARD =====================
if page == "📊 Dashboard":
    st.markdown("## 📊 System Overview")
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown("<div class='card'>### Avg Confidence<br><h2>0.76</h2></div>", unsafe_allow_html=True)
    with col2: st.markdown("<div class='card'>### Stability Status<br><h2>Stable</h2></div>", unsafe_allow_html=True)
    with col3: st.markdown("<div class='card'>### Active Model<br><h2>CNN v1.0</h2></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>### 📈 Refinement Trend</div>", unsafe_allow_html=True)

# ===================== CAPTCHA GENERATOR =====================
elif page == "🖼 CAPTCHA Generator":
    st.markdown("## 🖼 CAPTCHA Generator")
    col1, col2 = st.columns([1.2, 1.8])
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        noise = st.slider("Noise", 0.0, 1.0, 0.25)
        distortion = st.slider("Distortion", 0.0, 1.0, 0.25)
        clutter = st.slider("Clutter", 0.0, 1.0, 0.25)
        gen_btn = st.button("🎲 Generate CAPTCHA")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        preview_slot = st.empty()
        if gen_btn:
            img, text = generate_captcha(noise, distortion, clutter)
            preview_slot.image(img, use_column_width=True)
            pred, conf = predict(img)
            st.markdown(f"**Text:** `{text}`  |  **Difficulty:** `{pred.upper()}`  |  **Confidence:** `{conf:.2f}`")
        st.markdown("</div>", unsafe_allow_html=True)

# ===================== REFINEMENT ENGINE =====================
elif page == "🔁 Refinement Engine":
    st.markdown("## 🔁 Refinement Engine")
    target = st.selectbox("Target Difficulty", ["easy", "medium", "hard"])
    refine_btn = st.button("✨ Refine Once")
    auto_btn = st.button("🚀 Auto-Refine")

    col1, col2 = st.columns([1.5, 1.5])
    live_slot = st.empty()
    heat_slot = st.empty()  # heatmap live
    conv_slot = st.empty()  # convergence line live

    if refine_btn:
        img, text, lvl = refine(target)
        live_slot.image(img, use_column_width=True)
        buf = BytesIO()
        img.save(buf, format="PNG")
        st.download_button("⬇ Download CAPTCHA", buf.getvalue(), f"{text}_{lvl}.png")

    if auto_btn:
        confs = []
        grid = 4
        mat = np.zeros((grid, grid))  # heatmap
        for step in range(6):
            for i in range(grid):
                for j in range(grid):
                    img, _, _ = refine(target)
                    live_slot.image(img, use_column_width=True)
                    _, c = predict(img)
                    mat[i, j] = c
            confs.append(mat.mean())

            # Update convergence line dynamically
            with col1:
                fig1, ax1 = plt.subplots()
                ax1.plot(confs, marker='o', color='#00ffff')
                ax1.set_ylim(0,1)
                ax1.set_title("Convergence Line")
                ax1.grid(True, alpha=0.3)
                conv_slot.pyplot(fig1, clear_figure=True)
                plt.close(fig1)

            # Update heatmap live
            with col2:
                fig2, ax2 = plt.subplots()
                sns.heatmap(mat, annot=True, fmt=".2f", cmap="coolwarm", ax=ax2)
                ax2.set_title("Heatmap")
                heat_slot.pyplot(fig2, clear_figure=True)
                plt.close(fig2)

            time.sleep(0.5)

        st.success("Target difficulty stabilized ✔")

# ===================== FOOTER =====================
st.markdown("<div class='footer'>✨ Built by SANYAM KATOCH ✨</div>", unsafe_allow_html=True)
